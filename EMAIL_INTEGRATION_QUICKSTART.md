# Email Integration Quick Start

## Overview

Email integration enables your ERPNext multi-agent system to:
- 📧 Send quotations, invoices, and notifications
- 📥 Process incoming emails automatically
- 🤖 Email-enabled AI agents
- 🔄 Auto-create leads from emails

## Quick Setup (5 minutes)

### 1. Configure Email

Edit `agent-setup/.env`:

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
```

**For Gmail:**
1. Enable 2-Factor Authentication
2. Generate App Password (Google Account → Security → App passwords)
3. Use the 16-character app password

### 2. Start Email-Enabled Server

```bash
cd agent-setup
python email-api-server.py
```

### 3. Create Email-Enabled Agent

**Using Python:**
```python
from email_agent_integration import EmailEnabledMultiAgentManager
# ... (see email-example-usage.py)
```

**Using API:**
```bash
curl -X POST http://localhost:8001/agents/create \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "email-001",
    "agent_name": "Email Manager",
    "claude_api_key": "your_key"
  }'
```

## Use Cases

### Send Quotation
```
User: "Send quotation QUO-00001 to customer@example.com"
Agent: [Sends email automatically]
```

### Process Incoming Emails
```
User: "Process incoming emails"
Agent: [Reads emails, creates leads in ERPNext]
```

### Send Invoice
```
User: "Email invoice INV-00001 to customer@example.com"
Agent: [Sends invoice email]
```

## API Endpoints

- `POST /email/send-quotation` - Send quotation
- `POST /email/send-invoice` - Send invoice
- `POST /email/send-notification` - Send notification
- `POST /email/process-incoming` - Process emails
- `GET /email/read` - Read emails

## Full Documentation

See [agent-setup/EMAIL_SETUP.md](agent-setup/EMAIL_SETUP.md) for complete setup guide.
