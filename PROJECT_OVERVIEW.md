# DoganSystem - ERPNext v16 with Multi-Agent AI System

## Project Overview

This project provides a complete setup for **ERPNext v16** as a backend office system, operated by **multiple Claude AI agents** in a multi-agent environment.

## What's Included

### 1. ERPNext v16 Installation
- Complete installation guide for Windows, Linux, and macOS
- Server deployment instructions
- Production configuration
- Troubleshooting guides

### 2. Multi-Agent AI System
- Multiple Claude AI agents can operate ERPNext concurrently
- Natural language interface to ERPNext
- REST API for agent operations
- Agent orchestration system

### 3. Autonomous Workplace System ⭐ NEW
- **Zero human intervention** - Fully autonomous operations
- **Self-healing system** - Automatically detects and fixes issues
- **Auto-workflows** - Business processes run automatically
- **Intelligent automation** - AI agents make decisions autonomously
- **Auto-email processing** - Emails processed and leads created automatically
- **Continuous monitoring** - 24/7 system health monitoring

## Project Structure

```
DoganSystem/
├── README.md                    # Main ERPNext setup guide
├── SETUP.md                     # Quick setup reference
├── PREREQUISITES.md             # Prerequisites checklist
├── MULTI_AGENT_QUICKSTART.md    # Quick start for agents
├── AUTONOMOUS_WORKPLACE_SETUP.md # Autonomous system setup
├── PROJECT_OVERVIEW.md          # This file
│
└── agent-setup/                 # Multi-agent system
    ├── README.md                # Agent system overview
    ├── AGENT_SETUP.md          # Complete agent setup guide
    ├── agent-orchestrator.py   # Multi-agent orchestration
    ├── claude-agent-integration.py  # Claude AI integration
    ├── autonomous-orchestrator.py  # Autonomous system orchestrator
    ├── autonomous-workflow.py  # Workflow automation engine
    ├── self-healing-system.py  # Self-healing and monitoring
    ├── api-server.py           # REST API server
    ├── email-api-server.py     # Email-enabled API server
    ├── example-usage.py         # Usage examples
    ├── start-autonomous.sh     # Start autonomous system (Linux/Mac)
    ├── start-autonomous.ps1    # Start autonomous system (Windows)
    ├── requirements.txt         # Python dependencies
    ├── setup-agents.sh         # Linux/Mac setup
    ├── setup-agents.ps1        # Windows setup
    ├── erpnext-api-config.json # API configuration
    └── env.example             # Environment template
```

## Quick Start Guide

### Step 1: Install ERPNext v16

**Windows:**
1. Install prerequisites (Python, Node.js, MariaDB, Redis, Git, wkhtmltopdf)
2. Install bench: `pip install frappe-bench`
3. Initialize: `bench init --frappe-branch version-16 frappe-bench`
4. Get ERPNext: `bench get-app erpnext --branch version-16`
5. Create site: `bench new-site mysite.local`
6. Install: `bench --site mysite.local install-app erpnext`
7. Start: `bench start`

**See README.md for detailed instructions**

### Step 2: Set Up Multi-Agent System

1. **Navigate to agent directory:**
   ```bash
   cd agent-setup
   ```

2. **Run setup script:**
   ```powershell
   # Windows
   .\setup-agents.ps1
   
   # Linux/Mac
   ./setup-agents.sh
   ```

3. **Configure environment:**
   - Copy `env.example` to `.env`
   - Add your API keys:
     - ERPNext API Key (generate in ERPNext)
     - Claude API Key (from Anthropic)

4. **Start API server:**
   ```bash
   python api-server.py
   ```

5. **Create and use agents:**
   - See `example-usage.py` for Python examples
   - Or use REST API at `http://localhost:8001`

## Features

### ERPNext v16
- ✅ Complete ERP system (CRM, Sales, Inventory, Accounting, etc.)
- ✅ REST API access
- ✅ Customizable and extensible
- ✅ Production-ready deployment

### Multi-Agent System
- ✅ Multiple Claude agents working concurrently
- ✅ Natural language interface
- ✅ Specialized agents (Sales, Inventory, Accounting, etc.)
- ✅ REST API for integration
- ✅ Agent orchestration and task management
- ✅ Conversation context per agent
- ✅ **Email integration** - Send/receive emails, process automatically
- ✅ **Email-enabled agents** - Agents can handle email communications

## Use Cases

### Sales Agent
- "Show me all active customers"
- "Create a new quotation for customer ABC Corp"
- "What are the pending sales orders?"

### Inventory Agent
- "What's the stock level for item ITEM-001?"
- "Create a new item called Widget X"
- "Show me low stock items"

### Accounting Agent
- "Show me the chart of accounts"
- "Create a payment entry for $1000"
- "Generate sales report for this month"

## Documentation

- **ERPNext Setup**: [README.md](README.md)
- **Quick Setup**: [SETUP.md](SETUP.md)
- **Prerequisites**: [PREREQUISITES.md](PREREQUISITES.md)
- **Agent Quick Start**: [MULTI_AGENT_QUICKSTART.md](MULTI_AGENT_QUICKSTART.md)
- **Agent Full Guide**: [agent-setup/AGENT_SETUP.md](agent-setup/AGENT_SETUP.md)

## API Endpoints

When API server is running (`http://localhost:8001`):

- `POST /agents/create` - Create new agent
- `GET /agents` - List all agents
- `GET /agents/{agent_id}` - Get agent details
- `POST /agents/message` - Send message to agent
- `POST /erpnext/action` - Direct ERPNext action
- `GET /erpnext/resources` - List resource types

## Example Usage

### Python
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
    claude_api_key=os.getenv("CLAUDE_API_KEY")
)

# Use agent
response = agent.process_message("Show me all customers")
print(response)
```

### REST API
```bash
curl -X POST http://localhost:8001/agents/message \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "sales-001",
    "message": "Show me all active customers"
  }'
```

## System Requirements

- **RAM**: 4GB minimum (8GB+ recommended)
- **Storage**: 20GB+ free space
- **OS**: Windows 10/11, Linux (Ubuntu 20.04/22.04), macOS 11+
- **Python**: 3.10+
- **Node.js**: 18+
- **Database**: MariaDB 10.6+ or PostgreSQL 13+
- **Redis**: 6+

## Security Notes

- Store API keys securely (use `.env` file, never commit to git)
- Use HTTPS in production
- Implement authentication for production API server
- Use dedicated ERPNext user with appropriate permissions
- Set up rate limiting for agents

## Next Steps

1. ✅ Install ERPNext v16
2. ✅ Set up multi-agent system
3. ✅ Create specialized agents for your needs
4. ✅ Customize agent system prompts
5. ✅ Set up production deployment
6. ✅ Configure monitoring and logging
7. ✅ Implement additional integrations

## Support

- ERPNext Documentation: https://docs.erpnext.com/
- Frappe Framework: https://frappeframework.com/
- Claude API: https://docs.anthropic.com/
- Community Forum: https://discuss.erpnext.com/

## License

This setup guide and agent system are provided as-is. ERPNext is licensed under GNU GPL v3.
