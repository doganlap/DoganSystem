# ERPNext Multi-Agent System Setup Guide

This guide explains how to set up ERPNext as a backend office system operated by multiple Claude AI agents.

## Overview

The multi-agent system allows multiple Claude AI agents to:
- Interact with ERPNext through natural language
- Perform CRUD operations on ERPNext resources
- Execute custom Frappe methods
- Work concurrently with proper orchestration
- Maintain conversation context per agent

## Architecture

```
┌─────────────────┐
│  Claude Agents  │
│  (Multiple)     │
└────────┬────────┘
         │
         │ HTTP/REST API
         │
┌────────▼─────────────────┐
│  Multi-Agent API Server   │
│  (FastAPI)                │
└────────┬──────────────────┘
         │
         │ ERPNext API
         │
┌────────▼────────┐
│   ERPNext v16.2   │
│   Backend       │
└─────────────────┘
```

## Prerequisites

1. **ERPNext v16.2** installed and running
2. **Python 3.10+** installed
3. **Claude API Key** from Anthropic
4. **ERPNext API Key** generated in ERPNext

## Step 1: Generate ERPNext API Key

1. Login to your ERPNext instance
2. Go to **Settings > Integrations > API Keys**
3. Click **+ New**
4. Fill in:
   - **User**: Select a user (preferably a dedicated API user)
   - **Key Name**: e.g., "Multi-Agent System"
5. Click **Save**
6. **Copy the API Key and API Secret** (you'll need both)

## Step 2: Install Agent System

### Windows:
```powershell
cd agent-setup
.\setup-agents.ps1
```

### Linux/macOS:
```bash
cd agent-setup
chmod +x setup-agents.sh
./setup-agents.sh
```

## Step 3: Configure Environment

1. Edit `.env` file in `agent-setup/` directory:
```env
ERPNEXT_BASE_URL=http://localhost:8000
ERPNEXT_API_KEY=your_erpnext_api_key
ERPNEXT_API_SECRET=your_erpnext_api_secret
CLAUDE_API_KEY=your_claude_api_key
```

2. Replace the placeholder values with your actual credentials

## Step 4: Start API Server

### Windows:
```powershell
cd agent-setup
.\venv\Scripts\Activate.ps1
python api-server.py
```

### Linux/macOS:
```bash
cd agent-setup
source venv/bin/activate
python api-server.py
```

Or with uvicorn:
```bash
uvicorn api-server:app --host 0.0.0.0 --port 8001 --reload
```

The API server will start on `http://localhost:8001`

## Step 5: Create Agents

### Using Python:

```python
from claude_agent_integration import MultiAgentManager, ERPNextClient
import os

# Initialize
erpnext_client = ERPNextClient(
    base_url="http://localhost:8000",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

manager = MultiAgentManager(erpnext_client)

# Create specialized agents
sales_agent = manager.create_agent(
    agent_id="sales-001",
    agent_name="Sales Specialist",
    claude_api_key=os.getenv("CLAUDE_API_KEY"),
    system_prompt="You are a sales specialist. Help with customers, quotations, and sales orders."
)

inventory_agent = manager.create_agent(
    agent_id="inventory-001",
    agent_name="Inventory Manager",
    claude_api_key=os.getenv("CLAUDE_API_KEY"),
    system_prompt="You are an inventory manager. Help with items, stock, and warehouses."
)
```

### Using REST API:

```bash
# Create an agent
curl -X POST http://localhost:8001/agents/create \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "sales-001",
    "agent_name": "Sales Specialist",
    "claude_api_key": "your_claude_api_key",
    "system_prompt": "You are a sales specialist..."
  }'
```

## Step 6: Interact with Agents

### Using Python:

```python
# Send message to agent
response = sales_agent.process_message("Show me all active customers")
print(response)

# Agent will automatically:
# 1. Understand the request
# 2. Call ERPNext API
# 3. Return formatted response
```

### Using REST API:

```bash
# Send message
curl -X POST http://localhost:8001/agents/message \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "sales-001",
    "message": "Show me all active customers"
  }'
```

## Agent Capabilities

Each agent can:

1. **Retrieve Data**: "Show me all customers", "List active sales orders"
2. **Create Records**: "Create a new customer named ABC Corp"
3. **Update Records**: "Update customer CUST-001 email to new@email.com"
4. **Delete Records**: "Delete the test customer"
5. **Execute Methods**: "Run the sales report for this month"
6. **Complex Queries**: "Find all pending sales orders over $1000"

## Example Agent Interactions

### Sales Agent:
```
User: "Create a new customer called Tech Solutions Inc with email info@techsolutions.com"
Agent: "I'll create a new customer for you..."
[Agent creates customer via ERPNext API]
Agent: "Customer 'Tech Solutions Inc' has been created successfully with ID CUST-00123"
```

### Inventory Agent:
```
User: "What's the stock level for item ITEM-001?"
Agent: "Let me check the stock level..."
[Agent queries ERPNext]
Agent: "Item ITEM-001 currently has 150 units in stock across 2 warehouses."
```

## Multi-Agent Orchestration

The system supports multiple agents working simultaneously:

```python
from agent_orchestrator import AgentOrchestrator, Agent, ERPNextTask

# Initialize orchestrator
orchestrator = AgentOrchestrator(erpnext_client, max_agents=10)

# Register agents
agent1 = Agent(
    agent_id="agent-001",
    agent_name="Sales Agent",
    capabilities=["customer_management", "sales_order"],
    api_key="key-001"
)
orchestrator.register_agent(agent1)

# Submit tasks
task = ERPNextTask(
    task_id="task-001",
    agent_id="agent-001",
    action="get",
    resource_type="Customer",
    payload={"filters": {"status": "Active"}}
)
orchestrator.submit_task(task)

# Start orchestrator
orchestrator.start(num_workers=5)
```

## API Endpoints

### Agent Management
- `POST /agents/create` - Create a new agent
- `GET /agents` - List all agents
- `GET /agents/{agent_id}` - Get agent details

### Agent Interaction
- `POST /agents/message` - Send message to agent
- `POST /erpnext/action` - Direct ERPNext action

### ERPNext Resources
- `GET /erpnext/resources` - List available resource types

## Security Considerations

1. **API Keys**: Store securely, never commit to git
2. **Authentication**: Add authentication middleware for production
3. **Rate Limiting**: Configure rate limits per agent
4. **Permissions**: Use dedicated ERPNext user with appropriate permissions
5. **HTTPS**: Use HTTPS in production

## Production Deployment

1. **Use Environment Variables**: Never hardcode credentials
2. **Add Authentication**: Implement API key or OAuth
3. **Enable Logging**: Monitor agent activities
4. **Set Rate Limits**: Prevent abuse
5. **Use Process Manager**: PM2, supervisor, or systemd
6. **Enable HTTPS**: Use reverse proxy (nginx)

## Troubleshooting

### Agent not responding
- Check Claude API key is valid
- Verify ERPNext is accessible
- Check API server logs

### ERPNext connection errors
- Verify ERPNext API key and secret
- Check ERPNext base URL
- Ensure ERPNext user has proper permissions

### Import errors
- Activate virtual environment
- Install requirements: `pip install -r requirements.txt`

## Next Steps

1. Create specialized agents for different departments
2. Set up webhooks for real-time updates
3. Implement agent-to-agent communication
4. Add monitoring and analytics
5. Create custom Frappe methods for complex operations

## Support

For issues:
- Check ERPNext API documentation
- Review Claude API documentation
- Check logs in `agent-setup/logs/`
