"""
Example usage of ERPNext Multi-Agent System
Demonstrates how to use multiple agents with ERPNext
"""

import os
import json
from dotenv import load_dotenv
from claude_agent_integration import MultiAgentManager, ClaudeERPNextAgent
from agent_orchestrator import ERPNextClient

load_dotenv()


def main():
    # Load configuration
    erpnext_base_url = os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000")
    erpnext_api_key = os.getenv("ERPNEXT_API_KEY")
    erpnext_api_secret = os.getenv("ERPNEXT_API_SECRET")
    claude_api_key = os.getenv("CLAUDE_API_KEY")

    if not all([erpnext_api_key, erpnext_api_secret, claude_api_key]):
        print("ERROR: Please set ERPNEXT_API_KEY, ERPNEXT_API_SECRET, and CLAUDE_API_KEY in .env file")
        return

    # Initialize ERPNext client
    print("Initializing ERPNext client...")
    erpnext_client = ERPNextClient(
        base_url=erpnext_base_url,
        api_key=erpnext_api_key,
        api_secret=erpnext_api_secret
    )

    # Initialize multi-agent manager
    print("Initializing multi-agent manager...")
    manager = MultiAgentManager(erpnext_client)

    # Create specialized agents
    print("\nCreating agents...")

    # Sales Agent
    sales_agent = manager.create_agent(
        agent_id="sales-001",
        agent_name="Sales Specialist",
        claude_api_key=claude_api_key,
        system_prompt="""You are a sales specialist in ERPNext. Your responsibilities include:
- Managing customers and contacts
- Creating and managing quotations
- Processing sales orders
- Handling sales invoices
- Providing sales reports and analytics

Always be helpful, professional, and confirm important actions before executing them."""
    )
    print("✓ Sales Agent created")

    # Inventory Agent
    inventory_agent = manager.create_agent(
        agent_id="inventory-001",
        agent_name="Inventory Manager",
        claude_api_key=claude_api_key,
        system_prompt="""You are an inventory manager in ERPNext. Your responsibilities include:
- Managing items and item groups
- Monitoring stock levels
- Managing warehouses
- Processing stock entries
- Handling inventory reports

Always provide accurate stock information and warn about low stock levels."""
    )
    print("✓ Inventory Agent created")

    # Accounting Agent
    accounting_agent = manager.create_agent(
        agent_id="accounting-001",
        agent_name="Accounting Specialist",
        claude_api_key=claude_api_key,
        system_prompt="""You are an accounting specialist in ERPNext. Your responsibilities include:
- Managing chart of accounts
- Processing invoices
- Handling payment entries
- Generating financial reports
- Managing fiscal years

Always ensure accuracy in financial data and confirm before making changes."""
    )
    print("✓ Accounting Agent created")

    # Example interactions
    print("\n" + "="*60)
    print("Example Agent Interactions")
    print("="*60)

    # Example 1: Sales Agent
    print("\n[Sales Agent]")
    print("User: Show me all active customers")
    response = sales_agent.process_message("Show me all active customers")
    print(f"Agent: {response}\n")

    # Example 2: Inventory Agent
    print("[Inventory Agent]")
    print("User: What items do we have in stock?")
    response = inventory_agent.process_message("What items do we have in stock?")
    print(f"Agent: {response}\n")

    # Example 3: Accounting Agent
    print("[Accounting Agent]")
    print("User: Show me the chart of accounts")
    response = accounting_agent.process_message("Show me the chart of accounts")
    print(f"Agent: {response}\n")

    # List all agents
    print("\n" + "="*60)
    print("Registered Agents")
    print("="*60)
    agents = manager.list_agents()
    for agent in agents:
        print(f"- {agent['agent_name']} ({agent['agent_id']})")
        print(f"  Conversations: {agent['conversation_length']}")

    print("\nSetup complete! Agents are ready to use.")
    print("\nYou can now:")
    print("1. Use agents programmatically (as shown above)")
    print("2. Start the API server: python api-server.py")
    print("3. Use REST API to interact with agents")


if __name__ == "__main__":
    main()
