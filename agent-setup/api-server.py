"""
FastAPI server for multi-agent ERPNext operations
Provides REST API for agents to interact with ERPNext
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import logging

from claude_agent_integration import MultiAgentManager, ClaudeERPNextAgent
from agent_orchestrator import ERPNextClient

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ERPNext Multi-Agent API", version="1.0.0")

# CORS configuration - secure origins only
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "https://doganconsult.com,https://www.doganconsult.com,https://api.doganconsult.com,https://ai.doganconsult.com").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Tenant-ID", "X-Requested-With"],
)

# Initialize ERPNext client
erpnext_client = ERPNextClient(
    base_url=os.getenv("ERPNEXT_BASE_URL", "http://localhost:8000"),
    api_key=os.getenv("ERPNEXT_API_KEY", ""),
    api_secret=os.getenv("ERPNEXT_API_SECRET", "")
)

# Initialize multi-agent manager
agent_manager = MultiAgentManager(erpnext_client)


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


class ERPNextActionRequest(BaseModel):
    action: str  # get, create, update, delete, method
    resource_type: str
    agent_id: str
    payload: Dict[str, Any]


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "online",
        "service": "ERPNext Multi-Agent API",
        "version": "2.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker/Kubernetes"""
    return {
        "status": "healthy",
        "service": "agent-server",
        "version": "2.0.0",
        "agents_active": len(agent_manager.agents),
        "max_agents": int(os.getenv("MAX_AGENTS", 10)),
        "erpnext_configured": bool(os.getenv("ERPNEXT_API_KEY")),
        "claude_ready": bool(os.getenv("CLAUDE_API_KEY"))
    }


@app.post("/agents/create")
async def create_agent(request: AgentCreateRequest):
    """Create a new Claude agent"""
    try:
        agent = agent_manager.create_agent(
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
            "message": "Agent created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents")
async def list_agents():
    """List all registered agents"""
    agents = agent_manager.list_agents()
    return {
        "success": True,
        "agents": agents,
        "count": len(agents)
    }


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details"""
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {
        "success": True,
        "agent_id": agent.agent_id,
        "agent_name": agent.agent_name,
        "conversation_length": len(agent.conversation_history)
    }


@app.post("/agents/message")
async def send_message(request: MessageRequest):
    """Send a message to an agent and get response"""
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


@app.post("/erpnext/action")
async def erpnext_action(request: ERPNextActionRequest):
    """Execute direct ERPNext action"""
    agent = agent_manager.get_agent(request.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        result = None
        if request.action == "get":
            result = erpnext_client.get(
                resource_type=request.resource_type,
                filters=request.payload.get("filters"),
                fields=request.payload.get("fields")
            )
        elif request.action == "create":
            result = erpnext_client.post(
                resource_type=request.resource_type,
                data=request.payload.get("data", {})
            )
        elif request.action == "update":
            result = erpnext_client.put(
                resource_type=request.resource_type,
                name=request.payload.get("name"),
                data=request.payload.get("data", {})
            )
        elif request.action == "delete":
            result = erpnext_client.delete(
                resource_type=request.resource_type,
                name=request.payload.get("name")
            )
        elif request.action == "method":
            result = erpnext_client.execute_method(
                method_path=request.payload.get("method_path"),
                params=request.payload.get("params")
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown action: {request.action}")

        return {
            "success": True,
            "action": request.action,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error executing ERPNext action: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/erpnext/resources")
async def list_resources():
    """List available ERPNext resource types"""
    # Common ERPNext resources
    resources = [
        "Customer", "Supplier", "Item", "Sales Order", "Purchase Order",
        "Sales Invoice", "Purchase Invoice", "Quotation", "Lead", "Opportunity",
        "Contact", "Address", "Employee", "User", "Company", "Warehouse",
        "Stock Entry", "Delivery Note", "Purchase Receipt", "Payment Entry"
    ]
    return {
        "success": True,
        "resources": resources
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
