#!/usr/bin/env python3
"""
Quick Start Script for Claude Agent
Simple script to test Claude agent functionality
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_requirements():
    """Check if required packages are installed"""
    try:
        import anthropic
        print("[OK] Anthropic SDK installed")
    except ImportError:
        print("[!] Anthropic SDK not found. Installing...")
        os.system("pip install anthropic")
        import anthropic
        print("[OK] Anthropic SDK installed")
    
    try:
        # Try importing agent modules (may not be available if ERPNext not configured)
        try:
            import sys
            import importlib.util
            spec = importlib.util.spec_from_file_location("claude_agent_integration", "claude-agent-integration.py")
            if spec and spec.loader:
                claude_module = importlib.util.module_from_spec(spec)
                sys.modules["claude_agent_integration"] = claude_module
                spec.loader.exec_module(claude_module)
            print("[OK] Agent modules available (ERPNext integration)")
        except:
            print("[INFO] Agent modules not available (ERPNext integration optional)")
        return True
    except Exception as e:
        print(f"[INFO] Some modules not available: {e}")
        print("This is OK - basic Claude functionality will still work")
        return True

def test_claude_connection():
    """Test Claude API connection"""
    api_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("[!] Claude API key not found in .env file")
        print("Please set CLAUDE_API_KEY in agent-setup/.env")
        return False
    
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        # Simple test message - try different model names
        model_names = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-20240620", 
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
        
        message = None
        last_error = None
        
        for model in model_names:
            try:
                message = client.messages.create(
                    model=model,
                    max_tokens=100,
                    messages=[{
                        "role": "user",
                        "content": "Say 'Hello, I am ready to work!'"
                    }]
                )
                print(f"   Using model: {model}")
                break
            except Exception as e:
                last_error = e
                continue
        
        if not message:
            raise last_error
        
        response_text = message.content[0].text
        print(f"[OK] Claude API connection successful!")
        print(f"   Response: {response_text}")
        return True
    except Exception as e:
        print(f"[!] Claude API connection failed: {e}")
        return False

def create_simple_agent():
    """Create a simple Claude agent"""
    api_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ API key not found")
        return None
    
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        print("\n[INFO] Creating a simple Claude agent...")
        print("   Agent ID: simple-agent-001")
        print("   Agent Name: Simple Assistant")
        
        # Test with a simple message
        model_names = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-20240620",
            "claude-3-haiku-20240307",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229"
        ]
        
        message = None
        model_used = None
        
        for model in model_names:
            try:
                message = client.messages.create(
                    model=model,
                    max_tokens=500,
                    system="You are a helpful AI assistant for the DoganSystem.",
                    messages=[{
                        "role": "user",
                        "content": "Introduce yourself and explain what you can help with."
                    }]
                )
                model_used = model
                break
            except:
                continue
        
        if not message:
            raise Exception("No available Claude model found")
        
        response = message.content[0].text
        print(f"\n[OK] Agent created and tested!")
        print(f"\nAgent Response:\n{response}\n")
        
        return client
    except Exception as e:
        print(f"[!] Failed to create agent: {e}")
        return None

def interactive_chat(client):
    """Interactive chat with Claude agent"""
    if not client:
        return
    
    print("\n" + "="*60)
    print("Interactive Chat Mode")
    print("="*60)
    print("Type your messages (or 'quit' to exit)\n")
    
    conversation_history = []
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Try different models
            model_names = [
                "claude-3-5-sonnet-20241022",
                "claude-3-5-sonnet-20240620",
                "claude-3-haiku-20240307",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229"
            ]
            
            message = None
            for model in model_names:
                try:
                    message = client.messages.create(
                        model=model,
                        max_tokens=2000,
                        system="You are a helpful AI assistant for the DoganSystem. Be concise and helpful.",
                        messages=conversation_history[-10:]  # Last 10 messages for context
                    )
                    break
                except:
                    continue
            
            if not message:
                raise Exception("No available Claude model found")
            
            response = message.content[0].text
            conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            print(f"\nClaude: {response}\n")
            
        except Exception as e:
            print(f"[!] Error: {e}\n")

def main():
    """Main function"""
    print("="*60)
    print("Claude Agent Quick Start")
    print("="*60)
    print()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Test API connection
    if not test_claude_connection():
        sys.exit(1)
    
    # Create and test agent
    client = create_simple_agent()
    
    if client:
        # Ask if user wants interactive chat
        print("\n" + "="*60)
        choice = input("Start interactive chat? (y/n): ").strip().lower()
        
        if choice == 'y':
            interactive_chat(client)
        else:
            print("\n[OK] Claude agent is ready to use!")
            print("\nNext steps:")
            print("1. Use claude-agent-integration.py for ERPNext integration")
            print("2. Use claude_code_bridge.py for subagent employees")
            print("3. Start api-server.py for REST API access")

if __name__ == "__main__":
    main()
