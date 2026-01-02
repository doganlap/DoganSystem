"""
Email-Enabled Claude Agent Integration
Combines Claude AI with email capabilities for business management
"""

import os
import json
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from dotenv import load_dotenv
import logging

from claude_agent_integration import ClaudeERPNextAgent, MultiAgentManager
from agent_orchestrator import ERPNextClient
from email_integration import EmailManager, ERPNextEmailIntegration, EmailAgent

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailEnabledClaudeAgent(ClaudeERPNextAgent):
    """Claude agent with email capabilities"""

    def __init__(
        self,
        claude_api_key: str,
        erpnext_client: ERPNextClient,
        email_manager: EmailManager,
        agent_id: str,
        agent_name: str,
        system_prompt: Optional[str] = None
    ):
        super().__init__(claude_api_key, erpnext_client, agent_id, agent_name, system_prompt)

        # Initialize email integration
        self.erpnext_email = ERPNextEmailIntegration(erpnext_client, email_manager)
        self.email_agent = EmailAgent(self.erpnext_email, agent_name)

        # Update system prompt to include email capabilities
        self.system_prompt = self._enhanced_system_prompt()

    def _enhanced_system_prompt(self) -> str:
        """Enhanced system prompt with email capabilities"""
        base_prompt = super()._default_system_prompt()
        email_prompt = """

Additionally, you have email management capabilities:
- Send emails (quotations, invoices, notifications, custom emails)
- Read and process incoming emails
- Create leads/contacts from incoming emails
- Send welcome emails to new customers
- Send business notifications
- Manage email communications

Email operations available:
- send_quotation_email: Send quotation to customer
- send_invoice_email: Send invoice to customer
- send_customer_welcome_email: Welcome new customers
- send_notification_email: Send business notifications
- process_incoming_emails: Process and create leads from emails
- read_emails: Read emails from mailbox

When users request email operations, use the appropriate email functions.
"""
        return base_prompt + email_prompt

    def _email_tool_definitions(self) -> List[Dict]:
        """Email-related tool definitions for Claude"""
        return [
            {
                "name": "send_quotation_email",
                "description": "Send a quotation to a customer via email",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "quotation_name": {
                            "type": "string",
                            "description": "ERPNext quotation name/ID"
                        },
                        "recipient_email": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "custom_message": {
                            "type": "string",
                            "description": "Optional custom message"
                        }
                    },
                    "required": ["quotation_name", "recipient_email"]
                }
            },
            {
                "name": "send_invoice_email",
                "description": "Send an invoice to a customer via email",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "invoice_name": {
                            "type": "string",
                            "description": "ERPNext invoice name/ID"
                        },
                        "recipient_email": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "custom_message": {
                            "type": "string",
                            "description": "Optional custom message"
                        }
                    },
                    "required": ["invoice_name", "recipient_email"]
                }
            },
            {
                "name": "send_customer_welcome_email",
                "description": "Send welcome email to a new customer",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "customer_name": {
                            "type": "string",
                            "description": "ERPNext customer name/ID"
                        },
                        "recipient_email": {
                            "type": "string",
                            "description": "Customer email address"
                        }
                    },
                    "required": ["customer_name", "recipient_email"]
                }
            },
            {
                "name": "send_notification_email",
                "description": "Send a business notification email",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "recipient_email": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "notification_type": {
                            "type": "string",
                            "enum": ["order_confirmed", "payment_received", "shipment_sent", "invoice_due", "custom"],
                            "description": "Type of notification"
                        },
                        "message": {
                            "type": "string",
                            "description": "Notification message"
                        },
                        "reference_doctype": {
                            "type": "string",
                            "description": "Optional ERPNext document type"
                        },
                        "reference_name": {
                            "type": "string",
                            "description": "Optional ERPNext document name"
                        }
                    },
                    "required": ["recipient_email", "notification_type", "message"]
                }
            },
            {
                "name": "process_incoming_emails",
                "description": "Process incoming emails and create leads/contacts in ERPNext",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "read_emails",
                "description": "Read emails from mailbox",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Number of emails to read (default: 10)"
                        },
                        "unread_only": {
                            "type": "boolean",
                            "description": "Only read unread emails (default: false)"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "send_custom_email",
                "description": "Send a custom email",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject"
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body"
                        },
                        "cc": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "CC recipients"
                        },
                        "html": {
                            "type": "boolean",
                            "description": "Send as HTML (default: false)"
                        }
                    },
                    "required": ["to", "subject", "body"]
                }
            }
        ]

    def _execute_email_tool(self, tool_name: str, parameters: Dict) -> Dict:
        """Execute email tool"""
        try:
            if tool_name == "send_quotation_email":
                result = self.erpnext_email.send_quotation_email(
                    quotation_name=parameters["quotation_name"],
                    recipient_email=parameters["recipient_email"],
                    custom_message=parameters.get("custom_message")
                )
            elif tool_name == "send_invoice_email":
                result = self.erpnext_email.send_invoice_email(
                    invoice_name=parameters["invoice_name"],
                    recipient_email=parameters["recipient_email"],
                    custom_message=parameters.get("custom_message")
                )
            elif tool_name == "send_customer_welcome_email":
                result = self.erpnext_email.send_customer_welcome_email(
                    customer_name=parameters["customer_name"],
                    recipient_email=parameters["recipient_email"]
                )
            elif tool_name == "send_notification_email":
                result = self.erpnext_email.send_notification_email(
                    recipient_email=parameters["recipient_email"],
                    notification_type=parameters["notification_type"],
                    message=parameters["message"],
                    reference_doctype=parameters.get("reference_doctype"),
                    reference_name=parameters.get("reference_name")
                )
            elif tool_name == "process_incoming_emails":
                result = self.erpnext_email.process_incoming_emails()
                return {"success": True, "data": result}
            elif tool_name == "read_emails":
                emails = self.erpnext_email.email.read_emails(
                    limit=parameters.get("limit", 10),
                    unread_only=parameters.get("unread_only", False)
                )
                return {"success": True, "data": emails}
            elif tool_name == "send_custom_email":
                result = self.erpnext_email.email.send_email(
                    to=parameters["to"],
                    subject=parameters["subject"],
                    body=parameters["body"],
                    cc=parameters.get("cc"),
                    html=parameters.get("html", False)
                )
            else:
                return {"error": f"Unknown email tool: {tool_name}"}

            return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"Error executing email tool {tool_name}: {str(e)}")
            return {"success": False, "error": str(e)}

    def process_message(self, user_message: str, model: str = "claude-3-5-sonnet-20241022") -> str:
        """Process message with email capabilities"""
        # Get base tool definitions
        base_tools = super()._erpnext_tool_definitions()
        # Add email tools
        email_tools = self._email_tool_definitions()
        all_tools = base_tools + email_tools

        # Temporarily replace tools for this call
        original_method = self.claude.messages.create

        # Call parent method but with enhanced tools
        # We need to override the tool definitions
        try:
            # Add user message to conversation
            self.conversation_history.append({"role": "user", "content": user_message})

            # Call Claude with all tools (ERPNext + Email)
            message = self.claude.messages.create(
                model=model,
                max_tokens=4096,
                system=self.system_prompt,
                messages=self.conversation_history[-10:],
                tools=all_tools
            )

            # Process response
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
                # Check if it's an email tool or ERPNext tool
                if tool_call.name.startswith("erpnext_"):
                    # Use parent's ERPNext tool execution
                    tool_result = super()._execute_erpnext_tool(
                        tool_name=tool_call.name,
                        parameters=tool_call.input
                    )
                else:
                    # Use email tool execution
                    tool_result = self._execute_email_tool(
                        tool_name=tool_call.name,
                        parameters=tool_call.input
                    )

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": json.dumps(tool_result)
                })

            # If there were tool calls, get final response
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
                    messages=self.conversation_history[-10:],
                    tools=all_tools
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


class EmailEnabledMultiAgentManager(MultiAgentManager):
    """Multi-agent manager with email capabilities"""

    def __init__(self, erpnext_client: ERPNextClient, email_manager: EmailManager):
        super().__init__(erpnext_client)
        self.email_manager = email_manager

    def create_email_agent(
        self,
        agent_id: str,
        agent_name: str,
        claude_api_key: str,
        system_prompt: Optional[str] = None,
        capabilities: Optional[List[str]] = None
    ) -> EmailEnabledClaudeAgent:
        """Create an email-enabled Claude agent"""
        agent = EmailEnabledClaudeAgent(
            claude_api_key=claude_api_key,
            erpnext_client=self.erpnext,
            email_manager=self.email_manager,
            agent_id=agent_id,
            agent_name=agent_name,
            system_prompt=system_prompt
        )
        self.agents[agent_id] = agent
        logger.info(f"Created email-enabled agent: {agent_name} ({agent_id})")
        return agent
