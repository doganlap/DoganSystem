"""
FastAPI server with email capabilities for ERPNext multi-agent system
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import logging

from email_agent_integration import EmailEnabledMultiAgentManager, EmailEnabledClaudeAgent
from agent_orchestrator import ERPNextClient
from email_integration import EmailManager, ERPNextEmailIntegration

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ERPNext Email-Enabled Multi-Agent API", version="1.0.0")

# CORS configuration - secure origins only
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "https://doganconsult.com,https://www.doganconsult.com,https://api.doganconsult.com").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Tenant-ID", "X-Requested-With"],
)

# Initialize components
erpnext_client = ERPNextClient(
    base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000"),
    api_key=os.getenv("ERPNEXT_API_KEY", ""),
    api_secret=os.getenv("ERPNEXT_API_SECRET", "")
)

email_manager = EmailManager(
    smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    smtp_port=int(os.getenv("SMTP_PORT", "587")),
    smtp_username=os.getenv("SMTP_USERNAME", ""),
    smtp_password=os.getenv("SMTP_PASSWORD", ""),
    imap_server=os.getenv("IMAP_SERVER", "imap.gmail.com"),
    imap_port=int(os.getenv("IMAP_PORT", "993")),
    use_tls=os.getenv("SMTP_USE_TLS", "true").lower() == "true"
)

agent_manager = EmailEnabledMultiAgentManager(erpnext_client, email_manager)

# Request/Response models
class AgentCreateRequest(BaseModel):
    agent_id: str
    agent_name: str
    claude_api_key: str
    system_prompt: Optional[str] = None
    capabilities: Optional[List[str]] = None

class MessageRequest(BaseModel):
    message: str
    agent_id: str
    model: Optional[str] = "claude-3-5-sonnet-20241022"

class SendEmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    html: Optional[bool] = False

class SendQuotationEmailRequest(BaseModel):
    quotation_name: str
    recipient_email: EmailStr
    custom_message: Optional[str] = None

class SendInvoiceEmailRequest(BaseModel):
    invoice_name: str
    recipient_email: EmailStr
    custom_message: Optional[str] = None

class SendNotificationRequest(BaseModel):
    recipient_email: EmailStr
    notification_type: str
    message: str
    reference_doctype: Optional[str] = None
    reference_name: Optional[str] = None

# API Endpoints

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "ERPNext Email-Enabled Multi-Agent API",
        "version": "1.0.0",
        "features": ["erpnext", "email", "multi-agent", "claude-ai"]
    }

@app.post("/agents/create")
async def create_agent(request: AgentCreateRequest):
    """Create a new email-enabled agent"""
    try:
        agent = agent_manager.create_email_agent(
            agent_id=request.agent_id,
            agent_name=request.agent_name,
            claude_api_key=request.claude_api_key,
            system_prompt=request.system_prompt,
            capabilities=request.capabilities
        )
        return {
            "success": True,
            "agent_id": agent.agent_id,
            "agent_name": agent.agent_name,
            "message": "Email-enabled agent created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """List all agents"""
    agents = agent_manager.list_agents()
    return {
        "success": True,
        "agents": agents,
        "count": len(agents)
    }

@app.post("/agents/message")
async def send_message(request: MessageRequest):
    """Send message to agent"""
    agent = agent_manager.get_agent(request.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        response = agent.process_message(request.message, model=request.model)
        return {
            "success": True,
            "agent_id": request.agent_id,
            "response": response
        }
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Email endpoints

@app.post("/email/send")
async def send_email(request: SendEmailRequest):
    """Send a custom email"""
    try:
        result = email_manager.send_email(
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc,
            bcc=request.bcc,
            html=request.html
        )
        return result
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/email/send-quotation")
async def send_quotation_email(request: SendQuotationEmailRequest):
    """Send quotation via email"""
    try:
        erpnext_email = ERPNextEmailIntegration(erpnext_client, email_manager)
        result = erpnext_email.send_quotation_email(
            quotation_name=request.quotation_name,
            recipient_email=request.recipient_email,
            custom_message=request.custom_message
        )
        return result
    except Exception as e:
        logger.error(f"Error sending quotation email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/email/send-invoice")
async def send_invoice_email(request: SendInvoiceEmailRequest):
    """Send invoice via email"""
    try:
        erpnext_email = ERPNextEmailIntegration(erpnext_client, email_manager)
        result = erpnext_email.send_invoice_email(
            invoice_name=request.invoice_name,
            recipient_email=request.recipient_email,
            custom_message=request.custom_message
        )
        return result
    except Exception as e:
        logger.error(f"Error sending invoice email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/email/send-notification")
async def send_notification(request: SendNotificationRequest):
    """Send business notification email"""
    try:
        erpnext_email = ERPNextEmailIntegration(erpnext_client, email_manager)
        result = erpnext_email.send_notification_email(
            recipient_email=request.recipient_email,
            notification_type=request.notification_type,
            message=request.message,
            reference_doctype=request.reference_doctype,
            reference_name=request.reference_name
        )
        return result
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/email/process-incoming")
async def process_incoming_emails():
    """Process incoming emails and create leads"""
    try:
        erpnext_email = ERPNextEmailIntegration(erpnext_client, email_manager)
        processed = erpnext_email.process_incoming_emails()
        return {
            "success": True,
            "processed_count": len(processed),
            "details": processed
        }
    except Exception as e:
        logger.error(f"Error processing emails: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/email/read")
async def read_emails(limit: int = 10, unread_only: bool = False):
    """Read emails from mailbox"""
    try:
        emails = email_manager.read_emails(limit=limit, unread_only=unread_only)
        return {
            "success": True,
            "count": len(emails),
            "emails": emails
        }
    except Exception as e:
        logger.error(f"Error reading emails: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
