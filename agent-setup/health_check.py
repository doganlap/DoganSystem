"""
Comprehensive Health Check - Validates all system dependencies
"""

import os
import logging
from typing import Dict, Any, List
from datetime import datetime
import sqlite3

logger = logging.getLogger(__name__)


class HealthCheckStatus:
    """Health check status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthChecker:
    """Performs comprehensive health checks on all system dependencies"""

    def __init__(self):
        self.checks: List[Dict[str, Any]] = []

    async def check_all(self) -> Dict[str, Any]:
        """
        Performs all health checks and returns aggregated status.

        Returns:
            Dict with overall status and individual check results
        """
        results = {
            "status": HealthCheckStatus.HEALTHY,
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {},
            "summary": {
                "total": 0,
                "healthy": 0,
                "degraded": 0,
                "unhealthy": 0
            }
        }

        # Run all checks
        checks = [
            ("environment", self.check_environment_variables()),
            ("database", await self.check_database()),
            ("redis", await self.check_redis()),
            ("erpnext", await self.check_erpnext()),
            ("claude_api", await self.check_claude_api()),
            ("disk_space", self.check_disk_space()),
            ("memory", self.check_memory())
        ]

        # Aggregate results
        for check_name, check_result in checks:
            results["checks"][check_name] = check_result
            results["summary"]["total"] += 1

            status = check_result.get("status")
            if status == HealthCheckStatus.HEALTHY:
                results["summary"]["healthy"] += 1
            elif status == HealthCheckStatus.DEGRADED:
                results["summary"]["degraded"] += 1
                if results["status"] == HealthCheckStatus.HEALTHY:
                    results["status"] = HealthCheckStatus.DEGRADED
            else:  # UNHEALTHY
                results["summary"]["unhealthy"] += 1
                results["status"] = HealthCheckStatus.UNHEALTHY

        return results

    def check_environment_variables(self) -> Dict[str, Any]:
        """Check that critical environment variables are set"""
        try:
            required_vars = [
                "CLAUDE_API_KEY",
                "REDIS_HOST",
                "REDIS_PORT",
                "PLATFORM_DB_PATH"
            ]

            missing = []
            placeholder = []

            for var in required_vars:
                value = os.getenv(var)
                if not value:
                    missing.append(var)
                elif any(p in value.upper() for p in ["REPLACE", "TODO", "YOUR_", "CHANGEME"]):
                    placeholder.append(var)

            if missing or placeholder:
                return {
                    "status": HealthCheckStatus.UNHEALTHY,
                    "message": "Environment configuration issues detected",
                    "missing": missing,
                    "placeholder": placeholder
                }

            return {
                "status": HealthCheckStatus.HEALTHY,
                "message": "All required environment variables configured",
                "checked": len(required_vars)
            }

        except Exception as e:
            return {
                "status": HealthCheckStatus.UNHEALTHY,
                "message": f"Environment check failed: {str(e)}"
            }

    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and integrity"""
        try:
            platform_db = os.getenv("PLATFORM_DB_PATH", "platform.db")

            # Check if database file exists
            if not os.path.exists(platform_db):
                return {
                    "status": HealthCheckStatus.UNHEALTHY,
                    "message": "Platform database not found",
                    "path": platform_db
                }

            # Try to connect and query
            conn = sqlite3.connect(platform_db)
            cursor = conn.cursor()

            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            conn.close()

            if len(tables) == 0:
                return {
                    "status": HealthCheckStatus.DEGRADED,
                    "message": "Database exists but has no tables",
                    "tables": 0
                }

            return {
                "status": HealthCheckStatus.HEALTHY,
                "message": "Database connected successfully",
                "tables": len(tables),
                "path": platform_db
            }

        except Exception as e:
            return {
                "status": HealthCheckStatus.UNHEALTHY,
                "message": f"Database check failed: {str(e)}"
            }

    async def check_redis(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        try:
            import redis.asyncio as redis

            redis_host = os.getenv("REDIS_HOST", "localhost")
            redis_port = int(os.getenv("REDIS_PORT", "6379"))
            redis_password = os.getenv("REDIS_PASSWORD")

            # Create Redis client
            client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                socket_connect_timeout=5,
                decode_responses=True
            )

            # Test connection
            await client.ping()

            # Get info
            info = await client.info()
            await client.aclose()

            return {
                "status": HealthCheckStatus.HEALTHY,
                "message": "Redis connected successfully",
                "host": redis_host,
                "port": redis_port,
                "version": info.get("redis_version"),
                "uptime_seconds": info.get("uptime_in_seconds")
            }

        except ConnectionRefusedError:
            return {
                "status": HealthCheckStatus.UNHEALTHY,
                "message": "Redis connection refused",
                "host": redis_host,
                "port": redis_port
            }
        except Exception as e:
            return {
                "status": HealthCheckStatus.UNHEALTHY,
                "message": f"Redis check failed: {str(e)}"
            }

    async def check_erpnext(self) -> Dict[str, Any]:
        """Check ERPNext connectivity"""
        try:
            import aiohttp

            erpnext_url = os.getenv("ERPNEXT_BASE_URL")
            if not erpnext_url:
                return {
                    "status": HealthCheckStatus.DEGRADED,
                    "message": "ERPNext URL not configured"
                }

            # Check if ERPNext is accessible
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(f"{erpnext_url}/api/method/ping", timeout=5) as resp:
                        if resp.status == 200:
                            return {
                                "status": HealthCheckStatus.HEALTHY,
                                "message": "ERPNext accessible",
                                "url": erpnext_url,
                                "response_code": resp.status
                            }
                        else:
                            return {
                                "status": HealthCheckStatus.DEGRADED,
                                "message": "ERPNext responding with non-200 status",
                                "url": erpnext_url,
                                "response_code": resp.status
                            }
                except aiohttp.ClientConnectorError:
                    return {
                        "status": HealthCheckStatus.UNHEALTHY,
                        "message": "Cannot connect to ERPNext",
                        "url": erpnext_url
                    }

        except Exception as e:
            return {
                "status": HealthCheckStatus.DEGRADED,
                "message": f"ERPNext check failed: {str(e)}"
            }

    async def check_claude_api(self) -> Dict[str, Any]:
        """Check Claude API connectivity"""
        try:
            import anthropic

            api_key = os.getenv("CLAUDE_API_KEY")
            if not api_key or "REPLACE" in api_key.upper():
                return {
                    "status": HealthCheckStatus.UNHEALTHY,
                    "message": "Claude API key not configured"
                }

            # Note: We don't want to make actual API calls in health checks
            # as they cost money. Just validate the key format.
            if not api_key.startswith("sk-ant-"):
                return {
                    "status": HealthCheckStatus.UNHEALTHY,
                    "message": "Claude API key has invalid format"
                }

            return {
                "status": HealthCheckStatus.HEALTHY,
                "message": "Claude API key configured",
                "key_prefix": api_key[:10] + "..."
            }

        except Exception as e:
            return {
                "status": HealthCheckStatus.DEGRADED,
                "message": f"Claude API check failed: {str(e)}"
            }

    def check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space"""
        try:
            import shutil

            total, used, free = shutil.disk_usage("/")

            # Convert to GB
            total_gb = total // (2**30)
            used_gb = used // (2**30)
            free_gb = free // (2**30)
            percent_used = (used / total) * 100

            # Determine status based on usage
            if percent_used >= 90:
                status = HealthCheckStatus.UNHEALTHY
                message = "Disk space critically low"
            elif percent_used >= 80:
                status = HealthCheckStatus.DEGRADED
                message = "Disk space running low"
            else:
                status = HealthCheckStatus.HEALTHY
                message = "Disk space healthy"

            return {
                "status": status,
                "message": message,
                "total_gb": total_gb,
                "used_gb": used_gb,
                "free_gb": free_gb,
                "percent_used": round(percent_used, 2)
            }

        except Exception as e:
            return {
                "status": HealthCheckStatus.DEGRADED,
                "message": f"Disk space check failed: {str(e)}"
            }

    def check_memory(self) -> Dict[str, Any]:
        """Check available memory"""
        try:
            import psutil

            memory = psutil.virtual_memory()
            total_gb = memory.total / (1024**3)
            available_gb = memory.available / (1024**3)
            percent_used = memory.percent

            # Determine status
            if percent_used >= 95:
                status = HealthCheckStatus.UNHEALTHY
                message = "Memory critically low"
            elif percent_used >= 85:
                status = HealthCheckStatus.DEGRADED
                message = "Memory running low"
            else:
                status = HealthCheckStatus.HEALTHY
                message = "Memory healthy"

            return {
                "status": status,
                "message": message,
                "total_gb": round(total_gb, 2),
                "available_gb": round(available_gb, 2),
                "percent_used": round(percent_used, 2)
            }

        except ImportError:
            # psutil not installed, skip memory check
            return {
                "status": HealthCheckStatus.HEALTHY,
                "message": "Memory check skipped (psutil not installed)"
            }
        except Exception as e:
            return {
                "status": HealthCheckStatus.DEGRADED,
                "message": f"Memory check failed: {str(e)}"
            }


# Singleton instance
health_checker = HealthChecker()
