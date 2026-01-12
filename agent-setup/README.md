# ERPNext Multi-Agent System

This directory contains the multi-agent system that enables multiple Claude AI agents to operate ERPNext as a backend office system.

## Files Overview

### Core Files
- **`agent-orchestrator.py`** - Multi-agent orchestration system
- **`claude-agent-integration.py`** - Claude AI agent integration with ERPNext
- **`api-server.py`** - FastAPI REST server for agent operations
- **`erpnext-api-config.json`** - Configuration file for ERPNext API

### Setup Files
- **`setup-agents.sh`** - Linux/macOS setup script
- **`setup-agents.ps1`** - Windows setup script
- **`requirements.txt`** - Python dependencies
- **`env.example`** - Environment variables template

### Documentation
- **`AGENT_SETUP.md`** - Complete setup and usage guide
- **`example-usage.py`** - Example code demonstrating agent usage

## Quick Start

1. **Install dependencies:**
   ```bash
   # Windows
   .\setup-agents.ps1
   
   # Linux/Mac
   ./setup-agents.sh
   ```

2. **Configure environment:**
   - Copy `env.example` to `.env`
   - Add your ERPNext and Claude API keys

3. **Start API server:**
   ```bash
   python api-server.py
   ```

4. **Use agents:**
   - See `example-usage.py` for Python examples
   - Or use REST API at `http://localhost:8001`

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

## Documentation

- **Quick Start**: See [../MULTI_AGENT_QUICKSTART.md](../MULTI_AGENT_QUICKSTART.md)
- **Full Guide**: See [AGENT_SETUP.md](AGENT_SETUP.md)
- **Examples**: See [example-usage.py](example-usage.py)
