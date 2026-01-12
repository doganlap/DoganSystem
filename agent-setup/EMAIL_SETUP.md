# Email Integration Setup Guide

This guide explains how to set up email integration for the ERPNext multi-agent system to manage business needs.

## Overview

The email integration enables:
- ✅ Send emails (quotations, invoices, notifications)
- ✅ Receive and process incoming emails
- ✅ Auto-create leads/contacts from emails
- ✅ Email notifications for business events
- ✅ Email-enabled AI agents

## Prerequisites

1. **Email Account** (Gmail, Outlook, or custom SMTP)
2. **App Password** (for Gmail/Outlook)
3. **ERPNext v16.2** installed and running
4. **Multi-agent system** set up

## Step 1: Configure Email Account

### For Gmail:

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to Google Account → Security
   - Under "2-Step Verification", click "App passwords"
   - Generate password for "Mail"
   - Copy the 16-character password

3. **Update `.env` file**:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_USE_TLS=true
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
```

### For Outlook/Office 365:

```env
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=your_email@outlook.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true
IMAP_SERVER=outlook.office365.com
IMAP_PORT=993
```

### For Custom SMTP:

```env
SMTP_SERVER=mail.yourdomain.com
SMTP_PORT=587
SMTP_USERNAME=your_email@yourdomain.com
SMTP_PASSWORD=your_password
SMTP_USE_TLS=true
IMAP_SERVER=mail.yourdomain.com
IMAP_PORT=993
```

## Step 2: Install Email Dependencies

```bash
cd agent-setup
pip install -r requirements.txt
```

## Step 3: Start Email-Enabled API Server

```bash
# Activate virtual environment
# Windows: .\venv\Scripts\Activate.ps1
# Linux/Mac: source venv/bin/activate

python email-api-server.py
```

Or use uvicorn:
```bash
uvicorn email-api-server:app --host 0.0.0.0 --port 8001 --reload
```

## Step 4: Create Email-Enabled Agents

### Using Python:

```python
from email_agent_integration import EmailEnabledMultiAgentManager, ERPNextClient
from email_integration import EmailManager
import os

# Initialize ERPNext client
erpnext = ERPNextClient(
    base_url="http://localhost:8000",
    api_key=os.getenv("ERPNEXT_API_KEY"),
    api_secret=os.getenv("ERPNEXT_API_SECRET")
)

# Initialize email manager
email_manager = EmailManager(
    smtp_server=os.getenv("SMTP_SERVER"),
    smtp_port=int(os.getenv("SMTP_PORT")),
    smtp_username=os.getenv("SMTP_USERNAME"),
    smtp_password=os.getenv("SMTP_PASSWORD"),
    imap_server=os.getenv("IMAP_SERVER"),
    imap_port=int(os.getenv("IMAP_PORT"))
)

# Initialize manager
manager = EmailEnabledMultiAgentManager(erpnext, email_manager)

# Create email-enabled agent
agent = manager.create_email_agent(
    agent_id="business-001",
    agent_name="Business Email Manager",
    claude_api_key=os.getenv("CLAUDE_API_KEY"),
    system_prompt="You are a business email manager. Handle customer emails, send quotations, invoices, and notifications."
)
```

### Using REST API:

```bash
curl -X POST http://localhost:8001/agents/create \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "business-001",
    "agent_name": "Business Email Manager",
    "claude_api_key": "your_claude_key",
    "system_prompt": "You are a business email manager..."
  }'
```

## Email Capabilities

### 1. Send Quotation Email

**Using Agent:**
```
User: "Send quotation QUO-00001 to customer@example.com"
Agent: [Sends email with quotation details]
```

**Using API:**
```bash
curl -X POST http://localhost:8001/email/send-quotation \
  -H "Content-Type: application/json" \
  -d '{
    "quotation_name": "QUO-00001",
    "recipient_email": "customer@example.com"
  }'
```

### 2. Send Invoice Email

**Using Agent:**
```
User: "Email invoice INV-00001 to customer@example.com"
Agent: [Sends invoice email]
```

**Using API:**
```bash
curl -X POST http://localhost:8001/email/send-invoice \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_name": "INV-00001",
    "recipient_email": "customer@example.com"
  }'
```

### 3. Send Business Notifications

**Using Agent:**
```
User: "Send order confirmation notification to customer@example.com for order SO-00001"
Agent: [Sends notification email]
```

**Using API:**
```bash
curl -X POST http://localhost:8001/email/send-notification \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "customer@example.com",
    "notification_type": "order_confirmed",
    "message": "Your order has been confirmed",
    "reference_doctype": "Sales Order",
    "reference_name": "SO-00001"
  }'
```

### 4. Process Incoming Emails

**Using Agent:**
```
User: "Process incoming emails and create leads"
Agent: [Reads emails, creates leads/contacts in ERPNext]
```

**Using API:**
```bash
curl -X POST http://localhost:8001/email/process-incoming
```

### 5. Read Emails

**Using Agent:**
```
User: "Show me the last 10 emails"
Agent: [Reads and displays emails]
```

**Using API:**
```bash
curl -X GET "http://localhost:8001/email/read?limit=10&unread_only=true"
```

### 6. Send Custom Email

**Using Agent:**
```
User: "Send an email to customer@example.com with subject 'Welcome' and body 'Thank you for your business'"
Agent: [Sends custom email]
```

**Using API:**
```bash
curl -X POST http://localhost:8001/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "to": "customer@example.com",
    "subject": "Welcome",
    "body": "Thank you for your business",
    "html": false
  }'
```

## Business Use Cases

### Automated Customer Communication

1. **New Customer Welcome**
   - Automatically send welcome email when customer is created
   - Include account details and contact information

2. **Quotation Follow-up**
   - Send quotation immediately after creation
   - Follow up on pending quotations

3. **Invoice Reminders**
   - Send invoice when created
   - Remind customers of due payments

4. **Order Updates**
   - Confirm order receipt
   - Notify when order is shipped
   - Send delivery confirmation

5. **Lead Generation**
   - Process incoming emails
   - Auto-create leads from email inquiries
   - Route to appropriate sales agent

## Email Templates

You can customize email templates in the code:

```python
# In email-integration.py, modify the email body templates
# For example, quotation email:
body = f"""
Dear Customer,

Please find our quotation attached.

[Customize this template]
"""
```

## Automation Examples

### Auto-process Incoming Emails

Set up a cron job or scheduled task:

```python
# auto_process_emails.py
from email_integration import EmailManager, ERPNextEmailIntegration
from agent_orchestrator import ERPNextClient
import os

erpnext = ERPNextClient(...)
email_manager = EmailManager(...)
erpnext_email = ERPNextEmailIntegration(erpnext, email_manager)

# Process emails every hour
processed = erpnext_email.process_incoming_emails()
print(f"Processed {len(processed)} emails")
```

### Auto-send Quotations

```python
# When quotation is created in ERPNext
quotation_name = "QUO-00001"
customer_email = "customer@example.com"
erpnext_email.send_quotation_email(quotation_name, customer_email)
```

## API Endpoints

### Agent Management
- `POST /agents/create` - Create email-enabled agent
- `GET /agents` - List agents
- `POST /agents/message` - Send message to agent

### Email Operations
- `POST /email/send` - Send custom email
- `POST /email/send-quotation` - Send quotation
- `POST /email/send-invoice` - Send invoice
- `POST /email/send-notification` - Send notification
- `POST /email/process-incoming` - Process incoming emails
- `GET /email/read` - Read emails

## Troubleshooting

### Email not sending

1. **Check SMTP credentials**
   - Verify username and password
   - For Gmail, use App Password (not regular password)

2. **Check SMTP settings**
   - Verify server and port
   - Check TLS/SSL settings

3. **Check firewall**
   - Ensure SMTP port is not blocked

### Cannot read emails

1. **Check IMAP settings**
   - Verify IMAP server and port
   - Ensure IMAP is enabled in email account

2. **Check credentials**
   - Verify username and password

### Gmail App Password Issues

- Must enable 2-Factor Authentication first
- Generate new app password if old one doesn't work
- Use 16-character app password, not regular password

## Security Best Practices

1. **Use App Passwords** - Never use your main account password
2. **Store credentials securely** - Use `.env` file, never commit to git
3. **Enable TLS/SSL** - Always use encrypted connections
4. **Limit access** - Use dedicated email account for business
5. **Monitor logs** - Check email sending logs regularly

## Next Steps

1. ✅ Configure email account
2. ✅ Test email sending
3. ✅ Set up automated email processing
4. ✅ Create email-enabled agents
5. ✅ Customize email templates
6. ✅ Set up scheduled tasks for email automation

## Support

- Check email server logs
- Verify SMTP/IMAP settings
- Test with email client first
- Review error messages in API responses
