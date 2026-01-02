"""
Multi-Agent Orchestrator for ERPNext Operations
Manages multiple AI agents working with ERPNext backend
"""

import requests
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import threading
from queue import Queue
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Agent:
    """Represents an AI agent"""
    agent_id: str
    agent_name: str
    capabilities: List[str]
    api_key: str
    status: str = "idle"
    last_activity: Optional[datetime] = None


@dataclass
class ERPNextTask:
    """Represents a task to be executed in ERPNext"""
    task_id: str
    agent_id: str
    action: str
    resource_type: str
    payload: Dict
    priority: int = 5
    status: str = "pending"
    created_at: datetime = None


class ERPNextClient:
    """Client for interacting with ERPNext API"""

    def __init__(self, base_url: str, api_key: str, api_secret: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {api_key}:{api_secret}',
            'Content-Type': 'application/json'
        })

    def get(self, resource_type: str, filters: Optional[Dict] = None, fields: Optional[List] = None):
        """GET resource from ERPNext"""
        url = f"{self.base_url}/api/resource/{resource_type}"
        params = {}
        if filters:
            params['filters'] = json.dumps(filters)
        if fields:
            params['fields'] = json.dumps(fields)

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, resource_type: str, data: Dict):
        """POST (create) resource in ERPNext"""
        url = f"{self.base_url}/api/resource/{resource_type}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, resource_type: str, name: str, data: Dict):
        """PUT (update) resource in ERPNext"""
        url = f"{self.base_url}/api/resource/{resource_type}/{name}"
        response = self.session.put(url, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, resource_type: str, name: str):
        """DELETE resource from ERPNext"""
        url = f"{self.base_url}/api/resource/{resource_type}/{name}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()

    def execute_method(self, method_path: str, params: Optional[Dict] = None):
        """Execute a Frappe method"""
        url = f"{self.base_url}/api/method/{method_path}"
        response = self.session.post(url, json=params or {})
        response.raise_for_status()
        return response.json()


class AgentOrchestrator:
    """Orchestrates multiple agents working with ERPNext"""

    def __init__(self, erpnext_client: ERPNextClient, max_agents: int = 10):
        self.erpnext = erpnext_client
        self.agents: Dict[str, Agent] = {}
        self.tasks: Queue = Queue()
        self.active_tasks: Dict[str, ERPNextTask] = {}
        self.max_agents = max_agents
        self.lock = threading.Lock()
        self.running = False

    def register_agent(self, agent: Agent):
        """Register a new agent"""
        with self.lock:
            if len(self.agents) >= self.max_agents:
                raise ValueError(f"Maximum agents limit ({self.max_agents}) reached")
            self.agents[agent.agent_id] = agent
            logger.info(f"Agent {agent.agent_name} ({agent.agent_id}) registered")

    def unregister_agent(self, agent_id: str):
        """Unregister an agent"""
        with self.lock:
            if agent_id in self.agents:
                del self.agents[agent_id]
                logger.info(f"Agent {agent_id} unregistered")

    def submit_task(self, task: ERPNextTask):
        """Submit a task for execution"""
        if task.created_at is None:
            task.created_at = datetime.now()
        self.tasks.put(task)
        logger.info(f"Task {task.task_id} submitted by agent {task.agent_id}")

    def execute_task(self, task: ERPNextTask) -> Dict:
        """Execute a task in ERPNext"""
        try:
            task.status = "executing"
            agent = self.agents.get(task.agent_id)
            if not agent:
                raise ValueError(f"Agent {task.agent_id} not found")

            agent.status = "busy"
            agent.last_activity = datetime.now()

            result = None
            if task.action == "get":
                result = self.erpnext.get(
                    task.resource_type,
                    filters=task.payload.get("filters"),
                    fields=task.payload.get("fields")
                )
            elif task.action == "create":
                result = self.erpnext.post(task.resource_type, task.payload.get("data", {}))
            elif task.action == "update":
                result = self.erpnext.put(
                    task.resource_type,
                    task.payload.get("name"),
                    task.payload.get("data", {})
                )
            elif task.action == "delete":
                result = self.erpnext.delete(
                    task.resource_type,
                    task.payload.get("name")
                )
            elif task.action == "method":
                result = self.erpnext.execute_method(
                    task.payload.get("method_path"),
                    task.payload.get("params")
                )
            else:
                raise ValueError(f"Unknown action: {task.action}")

            task.status = "completed"
            agent.status = "idle"
            logger.info(f"Task {task.task_id} completed successfully")
            return {"success": True, "result": result, "task_id": task.task_id}

        except Exception as e:
            task.status = "failed"
            if task.agent_id in self.agents:
                self.agents[task.agent_id].status = "idle"
            logger.error(f"Task {task.task_id} failed: {str(e)}")
            return {"success": False, "error": str(e), "task_id": task.task_id}

    def worker_thread(self):
        """Worker thread that processes tasks"""
        while self.running:
            try:
                task = self.tasks.get(timeout=1)
                self.active_tasks[task.task_id] = task
                result = self.execute_task(task)
                # Store result or send callback
                self.active_tasks.pop(task.task_id, None)
                self.tasks.task_done()
            except:
                continue

    def start(self, num_workers: int = 5):
        """Start the orchestrator"""
        self.running = True
        for i in range(num_workers):
            thread = threading.Thread(target=self.worker_thread, daemon=True)
            thread.start()
        logger.info(f"Orchestrator started with {num_workers} workers")

    def stop(self):
        """Stop the orchestrator"""
        self.running = False
        logger.info("Orchestrator stopped")

    def get_agent_status(self, agent_id: str) -> Dict:
        """Get status of an agent"""
        agent = self.agents.get(agent_id)
        if not agent:
            return {"error": "Agent not found"}
        return {
            "agent_id": agent.agent_id,
            "agent_name": agent.agent_name,
            "status": agent.status,
            "capabilities": agent.capabilities,
            "last_activity": agent.last_activity.isoformat() if agent.last_activity else None
        }

    def get_all_agents_status(self) -> List[Dict]:
        """Get status of all agents"""
        return [self.get_agent_status(agent_id) for agent_id in self.agents.keys()]


# Example usage
if __name__ == "__main__":
    # Load configuration
    with open('agent-setup/erpnext-api-config.json') as f:
        config = json.load(f)

    # Initialize ERPNext client
    erpnext_client = ERPNextClient(
        base_url=config['erpnext']['base_url'],
        api_key=config['erpnext']['api_key'],
        api_secret=config['erpnext']['api_secret']
    )

    # Initialize orchestrator
    orchestrator = AgentOrchestrator(erpnext_client, max_agents=config['agents']['max_concurrent_agents'])

    # Register agents
    agent1 = Agent(
        agent_id="agent-001",
        agent_name="Sales Agent",
        capabilities=["customer_management", "sales_order", "quotation"],
        api_key="agent-001-key"
    )
    orchestrator.register_agent(agent1)

    # Start orchestrator
    orchestrator.start(num_workers=5)

    # Example task
    task = ERPNextTask(
        task_id="task-001",
        agent_id="agent-001",
        action="get",
        resource_type="Customer",
        payload={"filters": {"status": "Active"}, "fields": ["name", "customer_name", "email"]}
    )
    orchestrator.submit_task(task)

    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        orchestrator.stop()
