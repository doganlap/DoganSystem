#!/bin/bash
# Start Unified DoganSystem
# Multi-Tenant + Autonomous + Employee Agents + KSA Localization

echo "==========================================="
echo "Starting Unified DoganSystem"
echo "Multi-Tenant + Autonomous + Employee Agents + KSA"
echo "==========================================="

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "⚠ Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Check environment file
if [ ! -f ".env" ]; then
    echo "⚠ .env file not found. Copying from env.example..."
    cp env.example .env
    echo "⚠ Please edit .env file with your configuration"
    exit 1
fi

# Check Python dependencies
echo "Checking dependencies..."
python3 -c "import requests, anthropic, fastapi, sqlite3" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Create directories
echo "Creating directories..."
mkdir -p tenant_databases
mkdir -p .cursor

# Start unified system
echo ""
echo "Starting unified orchestrator..."
echo "This will start:"
echo "  - Multi-tenant system"
echo "  - Autonomous workflows"
echo "  - Employee agents"
echo "  - KSA localization"
echo "  - Self-healing system"
echo "  - Email processing"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 unified-orchestrator.py
