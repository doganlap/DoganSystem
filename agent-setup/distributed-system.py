"""
Distributed System Components for Horizontal Scaling
Enables multi-node deployment and load distribution
"""

import asyncio
import aiohttp
import json
import time
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging
import os

from agent_orchestrator import ERPNextClient, AgentOrchestrator, ERPNextTask
from autonomous_workflow import AutonomousWorkflowEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Node:
    """Represents a node in the distributed system"""
    node_id: str
    node_url: str
    status: str = "healthy"  # healthy, unhealthy, down
    last_heartbeat: Optional[datetime] = None
    load: float = 0.0  # Current load (0.0 to 1.0)
    capacity: int = 100  # Maximum capacity


class DistributedAgentManager:
    """Manages agents across multiple nodes"""

    def __init__(self, nodes: List[Node], redis_host: str = "localhost"):
        self.nodes = {node.node_id: node for node in nodes}
        self.session: Optional[aiohttp.ClientSession] = None
        self.redis_host = redis_host

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def distribute_task(self, task: ERPNextTask, node_id: Optional[str] = None) -> Dict:
        """Distribute task to a node"""
        if node_id is None:
            node_id = self._select_best_node()

        node = self.nodes.get(node_id)
        if not node or node.status != "healthy":
            node_id = self._select_best_node()
            node = self.nodes.get(node_id)

        if not node:
            return {"success": False, "error": "No healthy nodes available"}

        try:
            async with self.session.post(
                f"{node.node_url}/api/tasks/execute",
                json={
                    "task_id": task.task_id,
                    "agent_id": task.agent_id,
                    "action": task.action,
                    "resource_type": task.resource_type,
                    "payload": task.payload
                }
            ) as response:
                result = await response.json()

                # Update node load
                if result.get("success"):
                    node.load = min(node.load + 0.1, 1.0)

                return result
        except Exception as e:
            logger.error(f"Error distributing task to node {node_id}: {str(e)}")
            node.status = "unhealthy"
            return {"success": False, "error": str(e)}

    def _select_best_node(self) -> Optional[str]:
        """Select best node using load balancing algorithm"""
        healthy_nodes = [
            (node_id, node) for node_id, node in self.nodes.items()
            if node.status == "healthy"
        ]

        if not healthy_nodes:
            return None

        # Select node with lowest load
        best_node = min(healthy_nodes, key=lambda x: x[1].load)
        return best_node[0]

    async def check_node_health(self, node_id: str) -> bool:
        """Check if a node is healthy"""
        node = self.nodes.get(node_id)
        if not node:
            return False

        try:
            async with self.session.get(f"{node.node_url}/health", timeout=5) as response:
                if response.status == 200:
                    node.status = "healthy"
                    node.last_heartbeat = datetime.now()
                    return True
                else:
                    node.status = "unhealthy"
                    return False
        except Exception as e:
            logger.error(f"Health check failed for node {node_id}: {str(e)}")
            node.status = "down"
            return False

    async def monitor_nodes(self):
        """Monitor all nodes periodically"""
        while True:
            for node_id in self.nodes.keys():
                await self.check_node_health(node_id)
            await asyncio.sleep(30)  # Check every 30 seconds


class DistributedWorkflowEngine:
    """Distributed workflow execution engine"""

    def __init__(self, nodes: List[Node], redis_host: str = "localhost"):
        self.nodes = nodes
        self.redis_host = redis_host
        self.workflow_assignments: Dict[str, str] = {}  # workflow_id -> node_id

    def assign_workflow(self, workflow_id: str) -> str:
        """Assign workflow to a node"""
        # Use consistent hashing for workflow assignment
        node_index = int(hashlib.md5(workflow_id.encode()).hexdigest(), 16) % len(self.nodes)
        node_id = self.nodes[node_index].node_id
        self.workflow_assignments[workflow_id] = node_id
        return node_id

    async def execute_workflow_distributed(self, workflow_id: str, node_id: str, trigger_data: Dict):
        """Execute workflow on assigned node"""
        node = next((n for n in self.nodes if n.node_id == node_id), None)
        if not node:
            return {"success": False, "error": "Node not found"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{node.node_url}/api/workflows/execute",
                json={
                    "workflow_id": workflow_id,
                    "trigger_data": trigger_data
                }
            ) as response:
                return await response.json()


class LoadBalancer:
    """Simple load balancer for API requests"""

    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.current_index = 0
        self.node_stats = {node.node_id: {"requests": 0, "errors": 0} for node in nodes}

    def get_next_node(self) -> Optional[Node]:
        """Get next node using round-robin"""
        if not self.nodes:
            return None

        node = self.nodes[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.nodes)
        self.node_stats[node.node_id]["requests"] += 1
        return node

    def get_least_loaded_node(self) -> Optional[Node]:
        """Get node with least load"""
        if not self.nodes:
            return None

        return min(self.nodes, key=lambda n: n.load)

    def record_error(self, node_id: str):
        """Record error for a node"""
        if node_id in self.node_stats:
            self.node_stats[node_id]["errors"] += 1


class NodeManager:
    """Manages node lifecycle and coordination"""

    def __init__(self, node_id: str, node_url: str):
        self.node_id = node_id
        self.node_url = node_url
        self.peer_nodes: List[Node] = []
        self.is_leader = False

    def register_peer(self, peer_node: Node):
        """Register a peer node"""
        if peer_node.node_id != self.node_id:
            self.peer_nodes.append(peer_node)

    async def elect_leader(self):
        """Elect leader node (simple election)"""
        # Simple leader election: node with lowest ID becomes leader
        all_nodes = [Node(self.node_id, self.node_url)] + self.peer_nodes
        sorted_nodes = sorted(all_nodes, key=lambda n: n.node_id)

        if sorted_nodes[0].node_id == self.node_id:
            self.is_leader = True
            logger.info(f"Node {self.node_id} elected as leader")
        else:
            self.is_leader = False

    async def synchronize_state(self, state: Dict):
        """Synchronize state with peer nodes"""
        if not self.is_leader:
            return

        # Leader broadcasts state to all peers
        async with aiohttp.ClientSession() as session:
            for peer in self.peer_nodes:
                try:
                    async with session.post(
                        f"{peer.node_url}/api/sync/state",
                        json=state,
                        timeout=5
                    ) as response:
                        if response.status == 200:
                            logger.info(f"State synchronized with {peer.node_id}")
                except Exception as e:
                    logger.error(f"Failed to sync with {peer.node_id}: {str(e)}")


# Example distributed system setup
if __name__ == "__main__":
    # Define nodes
    nodes = [
        Node(node_id="node1", node_url="http://node1:8001"),
        Node(node_id="node2", node_url="http://node2:8001"),
        Node(node_id="node3", node_url="http://node3:8001")
    ]

    # Initialize load balancer
    lb = LoadBalancer(nodes)

    # Initialize distributed manager
    async def run_distributed_system():
        async with DistributedAgentManager(nodes) as manager:
            # Start node monitoring
            asyncio.create_task(manager.monitor_nodes())

            # Example: Distribute a task
            task = ERPNextTask(
                task_id="task-001",
                agent_id="agent-001",
                action="get",
                resource_type="Customer",
                payload={"filters": {"status": "Active"}}
            )

            result = await manager.distribute_task(task)
            print(f"Task result: {result}")

    asyncio.run(run_distributed_system())
