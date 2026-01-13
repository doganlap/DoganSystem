"""
Claude AI Service
Integration with Anthropic Claude API for AI-powered operations
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClaudeAIService:
    """Service for interacting with Claude AI"""

    def __init__(self, api_key: str = None):
        """Initialize the Claude AI service

        Args:
            api_key: Anthropic API key. If not provided, uses ANTHROPIC_API_KEY env var
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')

        if not self.api_key:
            logger.warning("No Anthropic API key provided. Set ANTHROPIC_API_KEY environment variable.")
            self.client = None
        else:
            self.client = Anthropic(api_key=self.api_key)
            logger.info("Claude AI Service initialized successfully")

        # Default model
        self.default_model = "claude-sonnet-4-20250514"

    def is_configured(self) -> bool:
        """Check if the service is properly configured"""
        return self.client is not None

    async def chat(
        self,
        message: str,
        system_prompt: str = None,
        model: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Send a chat message to Claude

        Args:
            message: The user message
            system_prompt: Optional system prompt
            model: Model to use (default: claude-sonnet-4-20250514)
            max_tokens: Maximum tokens in response
            temperature: Response randomness (0-1)

        Returns:
            Dict with response content and metadata
        """
        if not self.is_configured():
            return {"error": "Claude AI not configured. Set ANTHROPIC_API_KEY."}

        try:
            response = self.client.messages.create(
                model=model or self.default_model,
                max_tokens=max_tokens,
                system=system_prompt or "You are a helpful AI assistant for DoganSystem.",
                messages=[
                    {"role": "user", "content": message}
                ],
                temperature=temperature
            )

            return {
                "success": True,
                "content": response.content[0].text,
                "model": response.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return {"success": False, "error": str(e)}

    def chat_sync(
        self,
        message: str,
        system_prompt: str = None,
        model: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Synchronous chat with Claude

        Args:
            message: The user message
            system_prompt: Optional system prompt
            model: Model to use
            max_tokens: Maximum tokens in response
            temperature: Response randomness

        Returns:
            Dict with response content and metadata
        """
        if not self.is_configured():
            return {"error": "Claude AI not configured. Set ANTHROPIC_API_KEY."}

        try:
            response = self.client.messages.create(
                model=model or self.default_model,
                max_tokens=max_tokens,
                system=system_prompt or "You are a helpful AI assistant for DoganSystem.",
                messages=[
                    {"role": "user", "content": message}
                ],
                temperature=temperature
            )

            return {
                "success": True,
                "content": response.content[0].text,
                "model": response.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return {"success": False, "error": str(e)}

    def analyze_data(
        self,
        data: Dict[str, Any],
        analysis_type: str = "general",
        custom_prompt: str = None
    ) -> Dict[str, Any]:
        """Analyze data using Claude

        Args:
            data: Data to analyze (will be converted to JSON)
            analysis_type: Type of analysis (general, sales, inventory, hr, etc.)
            custom_prompt: Optional custom analysis prompt

        Returns:
            Analysis results from Claude
        """
        prompts = {
            "general": "Analyze the following data and provide insights:",
            "sales": "Analyze this sales data and identify trends, opportunities, and recommendations:",
            "inventory": "Analyze this inventory data and identify stock issues, reorder needs, and optimization opportunities:",
            "hr": "Analyze this HR data and provide insights on workforce, performance, and recommendations:",
            "financial": "Analyze this financial data and provide insights on cash flow, profitability, and recommendations:",
            "crm": "Analyze this CRM data and identify customer trends, opportunities, and engagement strategies:"
        }

        system_prompt = """You are a business analyst AI for DoganSystem.
        Analyze data and provide actionable insights in JSON format with the following structure:
        {
            "summary": "Brief overview",
            "key_findings": ["finding1", "finding2"],
            "recommendations": ["rec1", "rec2"],
            "risks": ["risk1", "risk2"],
            "metrics": {"metric1": value, "metric2": value}
        }"""

        user_prompt = custom_prompt or prompts.get(analysis_type, prompts["general"])
        user_prompt += f"\n\nData:\n```json\n{json.dumps(data, indent=2)}\n```"

        return self.chat_sync(
            message=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3  # Lower temperature for analysis
        )

    def generate_workflow_task(
        self,
        workflow_name: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate a task description for a workflow

        Args:
            workflow_name: Name of the workflow
            context: Additional context for the task

        Returns:
            Generated task details
        """
        system_prompt = """You are an AI workflow manager for DoganSystem.
        Generate detailed task instructions for AI employees to execute.
        Include step-by-step actions, expected outcomes, and validation criteria."""

        prompt = f"Generate a detailed task for the workflow: {workflow_name}"
        if context:
            prompt += f"\n\nContext:\n```json\n{json.dumps(context, indent=2)}\n```"

        return self.chat_sync(
            message=prompt,
            system_prompt=system_prompt,
            temperature=0.5
        )

    def process_erpnext_action(
        self,
        action_type: str,
        doctype: str,
        data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process an ERPNext action with AI assistance

        Args:
            action_type: Type of action (create, update, analyze, validate)
            doctype: ERPNext DocType (Customer, Sales Order, etc.)
            data: Data for the action

        Returns:
            AI-processed result
        """
        system_prompt = f"""You are an ERPNext automation AI for DoganSystem.
        Help with {action_type} operations on {doctype} documents.
        Provide structured responses that can be directly used in ERPNext."""

        prompt = f"Help with {action_type} for {doctype}."
        if data:
            prompt += f"\n\nData:\n```json\n{json.dumps(data, indent=2)}\n```"

        return self.chat_sync(
            message=prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )


# Global instance
claude_service = ClaudeAIService()


# Flask API endpoints for Claude AI
def register_claude_routes(app):
    """Register Claude AI routes with Flask app"""
    from flask import request, jsonify

    @app.route('/api/ai/chat', methods=['POST'])
    def ai_chat():
        """Chat with Claude AI"""
        if not claude_service.is_configured():
            return jsonify({"error": "Claude AI not configured"}), 503

        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({"error": "Message required"}), 400

        result = claude_service.chat_sync(
            message=message,
            system_prompt=data.get('system_prompt'),
            temperature=data.get('temperature', 0.7)
        )

        return jsonify(result)

    @app.route('/api/ai/analyze', methods=['POST'])
    def ai_analyze():
        """Analyze data with Claude AI"""
        if not claude_service.is_configured():
            return jsonify({"error": "Claude AI not configured"}), 503

        data = request.get_json()
        analysis_data = data.get('data')
        analysis_type = data.get('type', 'general')

        if not analysis_data:
            return jsonify({"error": "Data required"}), 400

        result = claude_service.analyze_data(
            data=analysis_data,
            analysis_type=analysis_type,
            custom_prompt=data.get('prompt')
        )

        return jsonify(result)

    @app.route('/api/ai/status', methods=['GET'])
    def ai_status():
        """Check Claude AI service status"""
        return jsonify({
            "configured": claude_service.is_configured(),
            "model": claude_service.default_model,
            "timestamp": datetime.now().isoformat()
        })

    logger.info("Claude AI routes registered")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("CLAUDE AI SERVICE TEST")
    print("="*80 + "\n")

    if claude_service.is_configured():
        print("[OK] Claude AI Service is configured")
        print(f"Default Model: {claude_service.default_model}")

        # Test chat
        print("\nTesting chat...")
        result = claude_service.chat_sync("Hello! What can you help me with in DoganSystem?")
        if result.get("success"):
            print(f"Response: {result['content'][:200]}...")
            print(f"Tokens used: {result['usage']}")
        else:
            print(f"Error: {result.get('error')}")
    else:
        print("[!] Claude AI Service not configured")
        print("Set ANTHROPIC_API_KEY environment variable to enable")
        print("\nExample:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print("  # or add to .env file")

    print("\n" + "="*80)
