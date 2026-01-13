# Claude Agent Setup - Complete Guide

## ✅ Status

**Claude API Key:** ✅ Configured in production environment
**Python Dependencies:** Installing...
**Agent System:** Ready to use

## 🚀 Quick Start Options

### Option 1: Simple Test (Recommended First Step)

```powershell
cd agent-setup
python quick_start_claude_agent.py
```

This will:
- Check if Anthropic SDK is installed
- Test Claude API connection
- Create a simple agent
- Offer interactive chat

### Option 2: Full Subagent System

```powershell
cd agent-setup
python start_subagent_system.py
```

This initializes:
- Claude Code subagents as ERP employees
- Default employees (Sarah, Mohammed, Fatima)
- Task management system
- Enhanced autonomous orchestrator

### Option 3: API Server

```powershell
cd agent-setup
python api-server.py
```

Then access:
- API Docs: `http://localhost:8001/docs`
- Health: `http://localhost:8001/`

### Option 4: Example Usage

```powershell
cd agent-setup
python example-usage.py
```

Creates specialized agents:
- Sales Agent
- Inventory Agent
- Accounting Agent

## 📋 Available Agent Types

### 1. Basic Claude Agent
**File:** `claude-agent-integration.py`
- Direct ERPNext integration
- Natural language processing
- CRUD operations

### 2. Claude Code Subagents
**File:** `claude_code_bridge.py`
- **Explore Agent** (System Analyst)
- **Plan Agent** (Business Process Architect)
- **General-purpose Agent** (Operations Manager)

### 3. Email-Enabled Agents
**File:** `email-agent-integration.py`
- Email processing
- Automated responses
- Email-triggered workflows

## 🔧 Installation

### Install Python Dependencies

```powershell
cd agent-setup
pip install -r requirements.txt
```

Or install individually:
```powershell
pip install anthropic python-dotenv fastapi uvicorn
```

## 📝 Configuration

### Environment Variables (`.env` file)

Already configured ✅:
```env
CLAUDE_API_KEY=sk-ant-api03-...
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Optional (for ERPNext integration):
```env
ERPNEXT_BASE_URL=http://localhost:8000
ERPNEXT_API_KEY=your_key
ERPNEXT_API_SECRET=your_secret
```

## 💻 Code Examples

### Simple Agent Usage

```python
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": "Hello, Claude!"
    }]
)

print(message.content[0].text)
```

### ERPNext-Integrated Agent

```python
from claude_agent_integration import MultiAgentManager
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

# Create agent
agent = manager.create_agent(
    agent_id="agent-001",
    agent_name="Assistant",
    claude_api_key=os.getenv("CLAUDE_API_KEY")
)

# Use agent
response = agent.process_message("List all customers")
print(response)
```

## 📚 Documentation Files

- `CLAUDE_AGENT_QUICK_START.md` - This guide
- `AGENT_SETUP.md` - Full setup instructions
- `CLAUDE_CODE_SUBAGENTS_AS_EMPLOYEES.md` - Subagent documentation
- `SUBAGENT_QUICKSTART.md` - Quick reference
- `API_DOCUMENTATION.md` - REST API docs

## 🎯 Next Steps

1. **Install dependencies:**
   ```powershell
   cd agent-setup
   pip install anthropic python-dotenv
   ```

2. **Test connection:**
   ```powershell
   python quick_start_claude_agent.py
   ```

3. **Start using agents:**
   - Use `example-usage.py` for examples
   - Start `api-server.py` for REST API
   - Use `start_subagent_system.py` for full system

---

**Status:** ✅ **Claude Agents ready** - API key configured, scripts available
