#!/bin/bash
# Start Autonomous Workplace System
# Zero Human Intervention Mode

echo "==========================================="
echo "Starting DoganSystem Autonomous Workplace"
echo "Zero Human Intervention Mode"
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
python3 -c "import requests, anthropic, fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start autonomous system
echo ""
echo "Starting autonomous orchestrator..."
echo "Press Ctrl+C to stop"
echo ""

python3 autonomous-orchestrator.py
