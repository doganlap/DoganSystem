# Claude Agent Quick Start Guide

## 🚀 Quick Start

### Prerequisites
- ✅ Claude API Key configured (already done)
- ✅ Python 3.10+ installed
- ✅ ERPNext running (optional, for ERPNext integration)

## 📋 Available Claude Agent Types

### 1. **Basic Claude Agent** (`claude-agent-integration.py`)
- Direct ERPNext integration
- Natural language to ERPNext operations
- CRUD operations support

### 2. **Claude Code Subagents** (`claude_code_bridge.py`)
- Explore Agent (System Analyst)
- Plan Agent (Business Process Architect)
- General-purpose Agent (Operations Manager)

### 3. **Email-Enabled Agents** (`email-agent-integration.py`)
- Email processing capabilities
- Automated email responses
- Email-triggered workflows

## 🎯 Quick Start Options

### Option 1: Start Subagent System (Recommended)

```powershell
cd agent-setup
python start_subagent_system.py
```

This will:
- Initialize Claude Code subagents as ERP employees
- Create default employees (Sarah, Mohammed, Fatima)
- Set up task management system
- Start the agent bridge

### Option 2: Start API Server

```powershell
cd agent-setup
python api-server.py
```

This starts a FastAPI server with:
- REST API for agent management
- Endpoints for creating/managing agents
- Message processing endpoints

### Option 3: Use Example Scripts

```powershell
cd agent-setup
python example-usage.py
```

## 📝 Basic Usage Example

### Create and Use a Claude Agent

```python
from claude_agent_integration import MultiAgentManager, ClaudeERPNextAgent
from agent_orchestrator import ERPNextClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize
erpnext_client = ERPNextClient(
    base_url=os.getenv("ERPNEXT_BASE_URL"),
    api_key=os.getenv("ERPNEXT_API_KEY"),
    api_secret=os.getenv("ERPNEXT_API_SECRET")
)

manager = MultiAgentManager(erpnext_client)

# Create an agent
agent = manager.create_agent(
    agent_id="agent-001",
    agent_name="Sales Assistant",
    claude_api_key=os.getenv("CLAUDE_API_KEY"),
    system_prompt="You are a sales specialist..."
)

# Use the agent
response = agent.process_message("List all active customers")
print(response)
```

## 🔧 Configuration

### Environment Variables (`.env` file)

```env
# Already configured ✅
CLAUDE_API_KEY=sk-ant-api03-...
ANTHROPIC_API_KEY=sk-ant-api03-...

# ERPNext (if using)
ERPNEXT_BASE_URL=http://localhost:8000
ERPNEXT_API_KEY=your_key
ERPNEXT_API_SECRET=your_secret
```

## 📚 Available Scripts

1. **`start_subagent_system.py`** - Full subagent system startup
2. **`api-server.py`** - REST API server for agents
3. **`example-usage.py`** - Basic usage examples
4. **`subagent_examples.py`** - Subagent-specific examples
5. **`claude-agent-integration.py`** - Core agent implementation

## 🎯 Common Tasks

### List All Agents
```python
agents = manager.list_agents()
for agent in agents:
    print(f"{agent['agent_name']} ({agent['agent_id']})")
```

### Process a Message
```python
response = agent.process_message("What customers do we have?")
print(response)
```

### Create Specialized Agent
```python
sales_agent = manager.create_agent(
    agent_id="sales-001",
    agent_name="Sales Specialist",
    claude_api_key=os.getenv("CLAUDE_API_KEY"),
    system_prompt="You specialize in sales operations..."
)
```

## 📖 Documentation Files

- `AGENT_SETUP.md` - Full setup guide
- `CLAUDE_CODE_SUBAGENTS_AS_EMPLOYEES.md` - Subagent documentation
- `SUBAGENT_QUICKSTART.md` - Quick reference
- `API_DOCUMENTATION.md` - API endpoints

## 🚀 Next Steps

1. **Start the system:**
   ```powershell
   cd agent-setup
   python start_subagent_system.py
   ```

2. **Or start API server:**
   ```powershell
   cd agent-setup
   python api-server.py
   # Then access: http://localhost:8001/docs
   ```

3. **Test with examples:**
   ```powershell
   python example-usage.py
   ```

---

**Status:** ✅ **Claude Agents ready to use** - API key configured, all dependencies available
