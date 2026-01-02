"""
Example usage of Email-Enabled ERPNext Multi-Agent System
Demonstrates email capabilities for business needs
"""

import os
from dotenv import load_dotenv
from email_agent_integration import EmailEnabledMultiAgentManager
from agent_orchestrator import ERPNextClient
from email_integration import EmailManager

load_dotenv()


def main():
    print("="*60)
    print("Email-Enabled ERPNext Multi-Agent System")
    print("="*60)

    # Initialize ERPNext client
    print("\n1. Initializing ERPNext client...")
    erpnext_client = ERPNextClient(
        base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000"),
        api_key=os.getenv("ERPNEXT_API_KEY"),
        api_secret=os.getenv("ERPNEXT_API_SECRET")
    )
    print("✓ ERPNext client initialized")

    # Initialize email manager
    print("\n2. Initializing email manager...")
    email_manager = EmailManager(
        smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_username=os.getenv("SMTP_USERNAME"),
        smtp_password=os.getenv("SMTP_PASSWORD"),
        imap_server=os.getenv("IMAP_SERVER", "imap.gmail.com"),
        imap_port=int(os.getenv("IMAP_PORT", "993")),
        use_tls=os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    )
    print("✓ Email manager initialized")

    # Initialize multi-agent manager
    print("\n3. Initializing multi-agent manager...")
    manager = EmailEnabledMultiAgentManager(erpnext_client, email_manager)
    print("✓ Multi-agent manager initialized")

    # Create email-enabled agents
    print("\n4. Creating email-enabled agents...")

    # Business Email Manager
    business_agent = manager.create_email_agent(
        agent_id="business-email-001",
        agent_name="Business Email Manager",
        claude_api_key=os.getenv("CLAUDE_API_KEY"),
        system_prompt="""You are a business email manager. Your responsibilities include:
- Sending quotations and invoices to customers
- Processing incoming customer emails
- Sending business notifications
- Managing email communications
- Creating leads from email inquiries

Always be professional, helpful, and confirm important actions."""
    )
    print("✓ Business Email Manager created")

    # Customer Service Agent
    customer_service_agent = manager.create_email_agent(
        agent_id="customer-service-001",
        agent_name="Customer Service Agent",
        claude_api_key=os.getenv("CLAUDE_API_KEY"),
        system_prompt="""You are a customer service agent. Handle customer inquiries via email:
- Answer customer questions
- Process customer requests
- Send order updates
- Handle complaints and support requests
- Escalate complex issues

Be friendly, professional, and solution-oriented."""
    )
    print("✓ Customer Service Agent created")

    # Sales Email Agent
    sales_email_agent = manager.create_email_agent(
        agent_id="sales-email-001",
        agent_name="Sales Email Agent",
        claude_api_key=os.getenv("CLAUDE_API_KEY"),
        system_prompt="""You are a sales email specialist. Your tasks include:
- Sending quotations to prospects
- Following up on quotations
- Sending sales proposals
- Managing sales email communications
- Converting email inquiries to sales opportunities

Be persuasive but professional."""
    )
    print("✓ Sales Email Agent created")

    # Example interactions
    print("\n" + "="*60)
    print("Example Email Interactions")
    print("="*60)

    # Example 1: Send quotation
    print("\n[Business Email Manager]")
    print("User: Send quotation QUO-00001 to customer@example.com")
    try:
        response = business_agent.process_message(
            "Send quotation QUO-00001 to customer@example.com"
        )
        print(f"Agent: {response}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")

    # Example 2: Process incoming emails
    print("[Business Email Manager]")
    print("User: Process incoming emails and create leads")
    try:
        response = business_agent.process_message(
            "Process incoming emails and create leads from new inquiries"
        )
        print(f"Agent: {response}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")

    # Example 3: Read emails
    print("[Customer Service Agent]")
    print("User: Show me the last 5 unread emails")
    try:
        response = customer_service_agent.process_message(
            "Show me the last 5 unread emails"
        )
        print(f"Agent: {response}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")

    # Example 4: Send notification
    print("[Sales Email Agent]")
    print("User: Send order confirmation to customer@example.com for order SO-00001")
    try:
        response = sales_email_agent.process_message(
            "Send order confirmation notification to customer@example.com for order SO-00001"
        )
        print(f"Agent: {response}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")

    # List all agents
    print("\n" + "="*60)
    print("Registered Email-Enabled Agents")
    print("="*60)
    agents = manager.list_agents()
    for agent in agents:
        print(f"- {agent['agent_name']} ({agent['agent_id']})")
        print(f"  Conversations: {agent['conversation_length']}")

    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nEmail-enabled agents are ready to:")
    print("✓ Send quotations and invoices")
    print("✓ Process incoming emails")
    print("✓ Send business notifications")
    print("✓ Create leads from emails")
    print("✓ Manage email communications")
    print("\nStart the API server: python email-api-server.py")
    print("Or use agents programmatically as shown above")


if __name__ == "__main__":
    main()
