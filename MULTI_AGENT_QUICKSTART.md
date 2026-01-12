# ERPNext Multi-Agent System - Quick Start

## Overview

This system enables **multiple Claude AI agents** to operate ERPNext v16.2 as a backend office system. Agents can:
- Query ERPNext data using natural language
- Create, update, and delete records
- Execute custom operations
- Work concurrently with proper orchestration
- **Send and receive emails** (quotations, invoices, notifications)
- **Process incoming emails** and create leads automatically
- **Manage business communications** via email

## Architecture

```
Claude Agents → API Server → ERPNext Backend
```

## Prerequisites

1. ✅ ERPNext v16.2 installed and running
2. ✅ Python 3.10+ installed
3. ✅ Claude API key from Anthropic
4. ✅ ERPNext API key (generate in ERPNext)
5. ✅ Email account configured (Gmail, Outlook, or custom SMTP) - See [EMAIL_SETUP.md](agent-setup/EMAIL_SETUP.md)

## Step 1: Generate ERPNext API Key

1. Login to ERPNext: `http://localhost:8000`
2. Go to **Settings → Integrations → API Keys**
3. Click **+ New**
4. Create API key for a user
5. **Copy API Key and Secret**

## Step 2: Install Agent System

### Windows:
```powershell
cd agent-setup
.\setup-agents.ps1
```

### Linux/Mac:
```bash
cd agent-setup
chmod +x setup-agents.sh
./setup-agents.sh
```

## Step 3: Configure

Edit `agent-setup/.env`:
```env
ERPNEXT_BASE_URL=http://localhost:8000
ERPNEXT_API_KEY=your_erpnext_api_key
ERPNEXT_API_SECRET=your_erpnext_api_secret
CLAUDE_API_KEY=your_claude_api_key
```

## Step 4: Start API Server

```bash
cd agent-setup
# Activate virtual environment
# Windows: .\venv\Scripts\Activate.ps1
# Linux/Mac: source venv/bin/activate

python api-server.py
```

Server runs on: `http://localhost:8001`

## Step 5: Create and Use Agents

### Option A: Using Python

```python
from claude_agent_integration import MultiAgentManager, ERPNextClient
import os

# Initialize
erpnext = ERPNextClient(
    base_url="http://localhost:8000",
    api_key=os.getenv("ERPNEXT_API_KEY"),
    api_secret=os.getenv("ERPNEXT_API_SECRET")
)

manager = MultiAgentManager(erpnext)

# Create agent
agent = manager.create_agent(
    agent_id="sales-001",
    agent_name="Sales Agent",
    claude_api_key=os.getenv("CLAUDE_API_KEY"),
    system_prompt="You are a sales specialist..."
)

# Use agent
response = agent.process_message("Show me all customers")
print(response)
```

### Option B: Using REST API

```bash
# Create agent
curl -X POST http://localhost:8001/agents/create \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "sales-001",
    "agent_name": "Sales Agent",
    "claude_api_key": "your_key",
    "system_prompt": "You are a sales specialist..."
  }'

# Send message
curl -X POST http://localhost:8001/agents/message \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "sales-001",
    "message": "Show me all active customers"
  }'
```

## Example Agent Types

### Sales Agent
- Manages customers, quotations, sales orders
- Handles sales invoices
- Provides sales reports

### Inventory Agent
- Manages items and stock levels
- Handles warehouses
- Processes stock entries

### Accounting Agent
- Manages chart of accounts
- Processes invoices and payments
- Generates financial reports

## Example Interactions

```
User: "Create a new customer called ABC Corp"
Agent: "I'll create that customer for you..."
[Creates customer via ERPNext API]
Agent: "Customer 'ABC Corp' created successfully with ID CUST-00123"

User: "Show me all pending sales orders"
Agent: "Let me fetch that information..."
[Queries ERPNext]
Agent: "Found 5 pending sales orders: [list]"
```

## API Endpoints

- `POST /agents/create` - Create new agent
- `GET /agents` - List all agents
- `POST /agents/message` - Send message to agent
- `POST /erpnext/action` - Direct ERPNext action
- `GET /erpnext/resources` - List resource types

## Multiple Agents Working Together

The system supports multiple agents working simultaneously:

```python
# Create multiple specialized agents
sales_agent = manager.create_agent(...)
inventory_agent = manager.create_agent(...)
accounting_agent = manager.create_agent(...)

# All can work concurrently
# Each maintains its own conversation context
```

## Next Steps

1. See [agent-setup/AGENT_SETUP.md](agent-setup/AGENT_SETUP.md) for detailed documentation
2. Run `python example-usage.py` to see examples
3. Customize agent system prompts for your needs
4. Set up production deployment with authentication

## Troubleshooting

**Agent not responding?**
- Check Claude API key is valid
- Verify ERPNext is accessible
- Check API server logs

**ERPNext connection error?**
- Verify API key and secret
- Check ERPNext base URL
- Ensure user has proper permissions

**Import errors?**
- Activate virtual environment
- Run: `pip install -r requirements.txt`

## Support

- Full documentation: [agent-setup/AGENT_SETUP.md](agent-setup/AGENT_SETUP.md)
- ERPNext docs: https://docs.erpnext.com/
- Claude API docs: https://docs.anthropic.com/
