"""
Claude AI Agent Integration with ERPNext
Enables Claude agents to interact with ERPNext backend
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from agent_orchestrator import AgentOrchestrator, ERPNextClient, Agent, ERPNextTask
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClaudeERPNextAgent:
    """Claude AI agent integrated with ERPNext"""

    def __init__(
        self,
        claude_api_key: str,
        erpnext_client: ERPNextClient,
        agent_id: str,
        agent_name: str,
        system_prompt: Optional[str] = None
    ):
        self.claude = Anthropic(api_key=claude_api_key)
        self.erpnext = erpnext_client
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.conversation_history: List[Dict] = []

    def _default_system_prompt(self) -> str:
        """Default system prompt for ERPNext operations"""
        return """You are an AI assistant integrated with ERPNext backend system.
Your role is to help users interact with ERPNext through natural language.

Available ERPNext operations:
1. GET - Retrieve data (customers, items, sales orders, etc.)
2. CREATE - Create new records
3. UPDATE - Update existing records
4. DELETE - Delete records
5. METHOD - Execute custom Frappe methods

When users request ERPNext operations, translate them into appropriate API calls.
Always provide clear, helpful responses and confirm actions before executing destructive operations.

Common ERPNext resources:
- Customer
- Item
- Sales Order
- Purchase Order
- Invoice
- Quotation
- Lead
- Contact
- Address
- etc."""

    def _erpnext_tool_definitions(self) -> List[Dict]:
        """Define tools available to Claude for ERPNext operations"""
        return [
            {
                "name": "erpnext_get",
                "description": "Retrieve data from ERPNext. Use filters to search and fields to specify which columns to return.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": "ERPNext resource type (e.g., 'Customer', 'Item', 'Sales Order')"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Filters to apply (e.g., {'status': 'Active'})"
                        },
                        "fields": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Fields to return (e.g., ['name', 'customer_name', 'email'])"
                        }
                    },
                    "required": ["resource_type"]
                }
            },
            {
                "name": "erpnext_create",
                "description": "Create a new record in ERPNext",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": "ERPNext resource type"
                        },
                        "data": {
                            "type": "object",
                            "description": "Data for the new record"
                        }
                    },
                    "required": ["resource_type", "data"]
                }
            },
            {
                "name": "erpnext_update",
                "description": "Update an existing record in ERPNext",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": "ERPNext resource type"
                        },
                        "name": {
                            "type": "string",
                            "description": "Name/ID of the record to update"
                        },
                        "data": {
                            "type": "object",
                            "description": "Fields to update"
                        }
                    },
                    "required": ["resource_type", "name", "data"]
                }
            },
            {
                "name": "erpnext_delete",
                "description": "Delete a record from ERPNext. Use with caution!",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": "ERPNext resource type"
                        },
                        "name": {
                            "type": "string",
                            "description": "Name/ID of the record to delete"
                        }
                    },
                    "required": ["resource_type", "name"]
                }
            },
            {
                "name": "erpnext_method",
                "description": "Execute a custom Frappe method in ERPNext",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "method_path": {
                            "type": "string",
                            "description": "Method path (e.g., 'frappe.client.get')"
                        },
                        "params": {
                            "type": "object",
                            "description": "Parameters for the method"
                        }
                    },
                    "required": ["method_path"]
                }
            }
        ]

    def _execute_erpnext_tool(self, tool_name: str, parameters: Dict) -> Dict:
        """Execute ERPNext tool based on Claude's request"""
        try:
            if tool_name == "erpnext_get":
                result = self.erpnext.get(
                    resource_type=parameters["resource_type"],
                    filters=parameters.get("filters"),
                    fields=parameters.get("fields")
                )
            elif tool_name == "erpnext_create":
                result = self.erpnext.post(
                    resource_type=parameters["resource_type"],
                    data=parameters["data"]
                )
            elif tool_name == "erpnext_update":
                result = self.erpnext.put(
                    resource_type=parameters["resource_type"],
                    name=parameters["name"],
                    data=parameters["data"]
                )
            elif tool_name == "erpnext_delete":
                result = self.erpnext.delete(
                    resource_type=parameters["resource_type"],
                    name=parameters["name"]
                )
            elif tool_name == "erpnext_method":
                result = self.erpnext.execute_method(
                    method_path=parameters["method_path"],
                    params=parameters.get("params")
                )
            else:
                return {"error": f"Unknown tool: {tool_name}"}

            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Error executing {tool_name}: {str(e)}")
            return {"success": False, "error": str(e)}

    def process_message(self, user_message: str, model: str = "claude-3-5-sonnet-20241022") -> str:
        """Process user message and interact with ERPNext via Claude"""
        # Add user message to conversation
        self.conversation_history.append({"role": "user", "content": user_message})

        try:
            # Call Claude with tools
            message = self.claude.messages.create(
                model=model,
                max_tokens=4096,
                system=self.system_prompt,
                messages=self.conversation_history[-10:],  # Last 10 messages for context
                tools=self._erpnext_tool_definitions()
            )

            # Process Claude's response
            response_text = ""
            tool_calls = []

            for content_block in message.content:
                if content_block.type == "text":
                    response_text += content_block.text
                elif content_block.type == "tool_use":
                    tool_calls.append(content_block)

            # Execute tool calls
            tool_results = []
            for tool_call in tool_calls:
                tool_result = self._execute_erpnext_tool(
                    tool_name=tool_call.name,
                    parameters=tool_call.input
                )
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": json.dumps(tool_result)
                })

            # If there were tool calls, get final response from Claude
            if tool_results:
                self.conversation_history.append({
                    "role": "assistant",
                    "content": [{"type": "tool_use", **tc.__dict__} for tc in tool_calls]
                })
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

                # Get final response
                final_message = self.claude.messages.create(
                    model=model,
                    max_tokens=4096,
                    system=self.system_prompt,
                    messages=self.conversation_history[-10:]
                )

                for content_block in final_message.content:
                    if content_block.type == "text":
                        response_text = content_block.text

            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": response_text})

            return response_text

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return f"I encountered an error: {str(e)}. Please try again."


class MultiAgentManager:
    """Manages multiple Claude agents working with ERPNext"""

    def __init__(self, erpnext_client: ERPNextClient):
        self.erpnext = erpnext_client
        self.agents: Dict[str, ClaudeERPNextAgent] = {}

    def create_agent(
        self,
        agent_id: str,
        agent_name: str,
        claude_api_key: str,
        system_prompt: Optional[str] = None,
        capabilities: Optional[List[str]] = None
    ) -> ClaudeERPNextAgent:
        """Create and register a new Claude agent"""
        agent = ClaudeERPNextAgent(
            claude_api_key=claude_api_key,
            erpnext_client=self.erpnext,
            agent_id=agent_id,
            agent_name=agent_name,
            system_prompt=system_prompt
        )
        self.agents[agent_id] = agent
        logger.info(f"Created agent: {agent_name} ({agent_id})")
        return agent

    def get_agent(self, agent_id: str) -> Optional[ClaudeERPNextAgent]:
        """Get an agent by ID"""
        return self.agents.get(agent_id)

    def list_agents(self) -> List[Dict]:
        """List all registered agents"""
        return [
            {
                "agent_id": agent_id,
                "agent_name": agent.agent_name,
                "conversation_length": len(agent.conversation_history)
            }
            for agent_id, agent in self.agents.items()
        ]


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

    # Initialize multi-agent manager
    manager = MultiAgentManager(erpnext_client)

    # Create specialized agents
    sales_agent = manager.create_agent(
        agent_id="sales-agent-001",
        agent_name="Sales Specialist",
        claude_api_key=os.getenv("CLAUDE_API_KEY"),
        system_prompt="You are a sales specialist. Help users with customer management, quotations, and sales orders in ERPNext."
    )

    inventory_agent = manager.create_agent(
        agent_id="inventory-agent-001",
        agent_name="Inventory Manager",
        claude_api_key=os.getenv("CLAUDE_API_KEY"),
        system_prompt="You are an inventory manager. Help users with items, stock levels, and warehouse management in ERPNext."
    )

    # Example interaction
    response = sales_agent.process_message("Show me all active customers")
    print(response)
