#!/bin/bash
# Setup script for ERPNext multi-agent system

echo "==========================================="
echo "ERPNext Multi-Agent System Setup"
echo "==========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# Create directories
mkdir -p logs
mkdir -p data

echo ""
echo "==========================================="
echo "Setup Complete!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your ERPNext and Claude API credentials"
echo "2. Generate ERPNext API key:"
echo "   - Login to ERPNext"
echo "   - Go to Settings > Integrations > API Keys"
echo "   - Create new API key"
echo "3. Start the API server:"
echo "   source venv/bin/activate"
echo "   python api-server.py"
echo ""
echo "Or use uvicorn directly:"
echo "   uvicorn api-server:app --host 0.0.0.0 --port 8001 --reload"
echo ""
