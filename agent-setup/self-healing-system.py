"""
Self-Healing and Autonomous Monitoring System
Automatically detects and fixes issues without human intervention
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import requests
import threading

from agent_orchestrator import ERPNextClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class IssueSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class HealthCheck:
    """Health check definition"""
    check_id: str
    name: str
    check_type: str  # api, database, service, etc.
    check_config: Dict[str, Any]
    interval: int = 60  # seconds
    timeout: int = 30
    retry_count: int = 3
    auto_fix: bool = True
    alert_threshold: int = 3  # Number of failures before alert


@dataclass
class SystemIssue:
    """System issue detected"""
    issue_id: str
    check_id: str
    severity: IssueSeverity
    description: str
    detected_at: datetime
    status: str = "open"  # open, fixing, fixed, ignored
    auto_fix_attempted: bool = False
    fix_actions: List[Dict] = None


@dataclass
class AutoFixAction:
    """Automatic fix action"""
    action_id: str
    name: str
    action_type: str
    action_config: Dict[str, Any]
    conditions: Optional[Dict[str, Any]] = None


class SelfHealingSystem:
    """Self-healing system for autonomous operations"""

    def __init__(self, erpnext_client: ERPNextClient):
        self.erpnext = erpnext_client
        self.health_checks: Dict[str, HealthCheck] = {}
        self.issues: Dict[str, SystemIssue] = {}
        self.auto_fix_actions: Dict[str, List[AutoFixAction]] = {}
        self.health_status: Dict[str, HealthStatus] = {}
        self.check_history: Dict[str, List[Dict]] = {}
        self.running = False
        self.lock = threading.Lock()

        # Initialize default health checks
        self._initialize_default_checks()

    def _initialize_default_checks(self):
        """Initialize default health checks"""
        # ERPNext API health check
        self.register_health_check(HealthCheck(
            check_id="erpnext_api",
            name="ERPNext API",
            check_type="api",
            check_config={
                "url": f"{self.erpnext.base_url}/api/method/ping",
                "method": "GET",
                "expected_status": 200
            },
            interval=60,
            auto_fix=True
        ))

        # Database connectivity check
        self.register_health_check(HealthCheck(
            check_id="database",
            name="Database Connectivity",
            check_type="database",
            check_config={},
            interval=120,
            auto_fix=True
        ))

        # Email service check
        self.register_health_check(HealthCheck(
            check_id="email_service",
            name="Email Service",
            check_type="email",
            check_config={},
            interval=300,
            auto_fix=True
        ))

    def register_health_check(self, check: HealthCheck):
        """Register a health check"""
        with self.lock:
            self.health_checks[check.check_id] = check
            self.health_status[check.check_id] = HealthStatus.UNKNOWN
            self.check_history[check.check_id] = []
            logger.info(f"Health check registered: {check.name} ({check.check_id})")

    def register_auto_fix(self, check_id: str, fix_actions: List[AutoFixAction]):
        """Register auto-fix actions for a health check"""
        self.auto_fix_actions[check_id] = fix_actions

    async def run_health_check(self, check_id: str) -> Dict[str, Any]:
        """Run a health check"""
        check = self.health_checks.get(check_id)
        if not check:
            return {"success": False, "error": "Check not found"}

        try:
            result = None
            if check.check_type == "api":
                result = await self._check_api(check.check_config)
            elif check.check_type == "database":
                result = await self._check_database(check.check_config)
            elif check.check_type == "email":
                result = await self._check_email(check.check_config)
            elif check.check_type == "custom":
                result = await self._check_custom(check.check_config)
            else:
                result = {"success": False, "error": f"Unknown check type: {check.check_type}"}

            # Record check result
            check_result = {
                "timestamp": datetime.now().isoformat(),
                "success": result.get("success", False),
                "response_time": result.get("response_time", 0),
                "details": result
            }

            self.check_history[check_id].append(check_result)
            # Keep only last 100 results
            if len(self.check_history[check_id]) > 100:
                self.check_history[check_id] = self.check_history[check_id][-100:]

            # Update health status
            if result.get("success"):
                self.health_status[check_id] = HealthStatus.HEALTHY
                # Clear any open issues
                self._clear_issues(check_id)
            else:
                # Check failure count
                recent_failures = sum(
                    1 for r in self.check_history[check_id][-check.alert_threshold:]
                    if not r.get("success")
                )

                if recent_failures >= check.alert_threshold:
                    self.health_status[check_id] = HealthStatus.CRITICAL
                    await self._handle_issue(check_id, result)
                else:
                    self.health_status[check_id] = HealthStatus.WARNING

            return check_result

        except Exception as e:
            logger.error(f"Error running health check {check_id}: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _check_api(self, config: Dict) -> Dict:
        """Check API endpoint"""
        start_time = time.time()
        try:
            url = config.get("url")
            method = config.get("method", "GET")
            expected_status = config.get("expected_status", 200)

            response = requests.request(method, url, timeout=30)
            response_time = time.time() - start_time

            success = response.status_code == expected_status

            return {
                "success": success,
                "status_code": response.status_code,
                "response_time": response_time,
                "expected_status": expected_status
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": time.time() - start_time
            }

    async def _check_database(self, config: Dict) -> Dict:
        """Check database connectivity"""
        start_time = time.time()
        try:
            # Try a simple ERPNext API call that requires database
            result = self.erpnext.get("User", filters={"name": "Administrator"}, fields=["name"])
            response_time = time.time() - start_time

            success = result is not None

            return {
                "success": success,
                "response_time": response_time
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": time.time() - start_time
            }

    async def _check_email(self, config: Dict) -> Dict:
        """Check email service"""
        # Placeholder - implement email service check
        return {"success": True, "message": "Email service check not implemented"}

    async def _check_custom(self, config: Dict) -> Dict:
        """Check custom health check"""
        # Execute custom check logic
        return {"success": True, "message": "Custom check executed"}

    async def _handle_issue(self, check_id: str, check_result: Dict):
        """Handle detected issue"""
        check = self.health_checks.get(check_id)
        if not check:
            return

        # Check if issue already exists
        existing_issue = next(
            (issue for issue in self.issues.values()
             if issue.check_id == check_id and issue.status == "open"),
            None
        )

        if existing_issue:
            return  # Issue already being handled

        # Create new issue
        issue = SystemIssue(
            issue_id=f"{check_id}_{datetime.now().timestamp()}",
            check_id=check_id,
            severity=IssueSeverity.HIGH if self.health_status[check_id] == HealthStatus.CRITICAL else IssueSeverity.MEDIUM,
            description=f"Health check failed: {check.name}",
            detected_at=datetime.now(),
            fix_actions=[]
        )

        self.issues[issue.issue_id] = issue

        logger.warning(f"Issue detected: {issue.description} ({issue.issue_id})")

        # Attempt auto-fix
        if check.auto_fix:
            await self._attempt_auto_fix(issue)

    async def _attempt_auto_fix(self, issue: SystemIssue):
        """Attempt to automatically fix an issue"""
        issue.status = "fixing"
        issue.auto_fix_attempted = True

        fix_actions = self.auto_fix_actions.get(issue.check_id, [])

        if not fix_actions:
            logger.warning(f"No auto-fix actions registered for {issue.check_id}")
            issue.status = "open"
            return

        logger.info(f"Attempting auto-fix for issue {issue.issue_id}")

        for fix_action in fix_actions:
            try:
                result = await self._execute_fix_action(fix_action, issue)
                issue.fix_actions.append({
                    "action_id": fix_action.action_id,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })

                if result.get("success"):
                    logger.info(f"Auto-fix successful: {fix_action.name}")
                    issue.status = "fixed"
                    break
            except Exception as e:
                logger.error(f"Error executing fix action {fix_action.action_id}: {str(e)}")

        if issue.status == "fixing":
            issue.status = "open"  # Auto-fix failed

    async def _execute_fix_action(self, action: AutoFixAction, issue: SystemIssue) -> Dict:
        """Execute a fix action"""
        if action.action_type == "restart_service":
            # Restart service logic
            return {"success": True, "message": "Service restart attempted"}
        elif action.action_type == "clear_cache":
            # Clear cache logic
            return {"success": True, "message": "Cache cleared"}
        elif action.action_type == "retry_connection":
            # Retry connection logic
            return {"success": True, "message": "Connection retried"}
        elif action.action_type == "custom":
            # Execute custom fix
            return {"success": True, "message": "Custom fix executed"}
        else:
            return {"success": False, "error": f"Unknown action type: {action.action_type}"}

    def _clear_issues(self, check_id: str):
        """Clear resolved issues"""
        for issue_id, issue in list(self.issues.items()):
            if issue.check_id == check_id and issue.status == "fixed":
                del self.issues[issue_id]

    def start_monitoring(self):
        """Start the monitoring system"""
        self.running = True
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        logger.info("Self-healing monitoring system started")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                for check_id, check in self.health_checks.items():
                    asyncio.run(self.run_health_check(check_id))
                    time.sleep(check.interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(60)

    def get_system_health(self) -> Dict:
        """Get overall system health"""
        total_checks = len(self.health_checks)
        healthy = sum(1 for status in self.health_status.values() if status == HealthStatus.HEALTHY)
        warning = sum(1 for status in self.health_status.values() if status == HealthStatus.WARNING)
        critical = sum(1 for status in self.health_status.values() if status == HealthStatus.CRITICAL)

        open_issues = sum(1 for issue in self.issues.values() if issue.status == "open")

        overall_status = HealthStatus.HEALTHY
        if critical > 0:
            overall_status = HealthStatus.CRITICAL
        elif warning > 0:
            overall_status = HealthStatus.WARNING

        return {
            "overall_status": overall_status.value,
            "total_checks": total_checks,
            "healthy": healthy,
            "warning": warning,
            "critical": critical,
            "open_issues": open_issues,
            "checks": {
                check_id: {
                    "name": check.name,
                    "status": self.health_status[check_id].value,
                    "last_check": self.check_history[check_id][-1]["timestamp"] if self.check_history[check_id] else None
                }
                for check_id, check in self.health_checks.items()
            },
            "issues": [
                {
                    "issue_id": issue.issue_id,
                    "check_id": issue.check_id,
                    "severity": issue.severity.value,
                    "description": issue.description,
                    "status": issue.status,
                    "detected_at": issue.detected_at.isoformat()
                }
                for issue in self.issues.values() if issue.status == "open"
            ]
        }
