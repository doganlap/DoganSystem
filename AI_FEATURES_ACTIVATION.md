# AI Features Activation Guide

## Quick Status

| Feature | Config File | Status |
|---------|-------------|--------|
| Claude AI Agents | `.env` | NEEDS API KEY |
| ERPNext Integration | `.env` + `appsettings.json` | NEEDS API KEYS |
| Autonomous Workflows | `.env` | ENABLED |
| Self-Healing System | `.env` | ENABLED |
| Email Processing | `.env` | NEEDS SMTP CONFIG |
| Multi-Tenant | `.env` | ENABLED |
| Python Services | `requirements.txt` | READY |

---

## Step 1: Get Required API Keys

### Claude AI (REQUIRED)
1. Go to https://console.anthropic.com/
2. Create account or sign in
3. Go to API Keys section
4. Generate new API key
5. Copy and paste into `agent-setup/.env`:
   ```
   CLAUDE_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY
   ```

### ERPNext API (REQUIRED)
1. Login to your ERPNext instance as Administrator
2. Go to: Settings > Users > [Your User]
3. Scroll to "API Access" section
4. Click "Generate Keys"
5. Copy both API Key and API Secret
6. Update in `agent-setup/.env`:
   ```
   ERPNEXT_BASE_URL=http://your-erpnext-url:8000
   ERPNEXT_API_KEY=your_api_key
   ERPNEXT_API_SECRET=your_api_secret
   ```
7. Also update in `src/DoganSystem.Web.Mvc/appsettings.json`:
   ```json
   "ErpNext": {
     "DefaultUrl": "http://your-erpnext-url:8000",
     "ApiKey": "your_api_key",
     "ApiSecret": "your_api_secret"
   }
   ```

---

## Step 2: Install Python Dependencies

```bash
cd /root/CascadeProjects/DoganSystem/agent-setup
pip install -r requirements.txt
```

---

## Step 3: Start Services

### Terminal 1 - API Gateway (Main Entry Point)
```bash
cd /root/CascadeProjects/DoganSystem/agent-setup
uvicorn api-gateway:app --host 0.0.0.0 --port 8006 --reload
```

### Terminal 2 - Agent API Server
```bash
cd /root/CascadeProjects/DoganSystem/agent-setup
uvicorn api-server:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 3 - C# Web Application
```bash
cd /root/CascadeProjects/DoganSystem/src/DoganSystem.Web.Mvc
dotnet run
```

---

## Step 4: Verify Services

```bash
# Check API Gateway
curl http://localhost:8006/health

# Check Agent API
curl http://localhost:8001/health

# Check C# App
curl http://localhost:5000/
```

---

## AI Features Summary

### 1. Claude AI Agents
- Natural language processing for business tasks
- ERPNext CRUD operations via conversation
- Multi-turn conversation support

### 2. Autonomous Workflows
- Scheduled task execution
- Event-driven automation
- Conditional branching

### 3. Self-Healing System
- Automatic health monitoring
- Auto-recovery from failures
- Issue logging and alerting

### 4. Multi-Agent Orchestration
- 10 concurrent agents supported
- Task delegation between agents
- Team-based organization

### 5. Email Integration
- Email-triggered workflows
- Agent email notifications
- IMAP/SMTP support

---

## Configuration Files Location

```
/root/CascadeProjects/DoganSystem/
├── agent-setup/
│   ├── .env                      # Python services config (EDIT THIS)
│   ├── erpnext-api-config.json   # ERPNext API settings
│   └── requirements.txt          # Python dependencies
└── src/DoganSystem.Web.Mvc/
    └── appsettings.json          # C# app config (EDIT THIS)
```

---

## Troubleshooting

### "Claude API key invalid"
- Verify key starts with `sk-ant-`
- Check key hasn't expired
- Ensure no extra spaces in `.env`

### "ERPNext connection failed"
- Verify ERPNext URL is accessible
- Check API key/secret are correct
- Ensure API user has required permissions

### "Python service won't start"
- Run `pip install -r requirements.txt`
- Check port isn't already in use
- Verify `.env` file exists
