#!/bin/bash
# Git Setup Script for DoganSystem
# Run: chmod +x setup-git.sh && ./setup-git.sh

echo "==========================================="
echo "DoganSystem Git Setup"
echo "==========================================="
echo ""

# Check if git is installed
echo "Checking Git installation..."
if command -v git &> /dev/null; then
    echo "✓ Git found: $(git --version)"
else
    echo "✗ Git not found. Please install Git first."
    echo "Install: sudo apt-get install git"
    exit 1
fi

echo ""

# Initialize git repository
echo "Initializing Git repository..."
if [ -d ".git" ]; then
    echo "✓ Git repository already initialized"
else
    git init
    echo "✓ Git repository initialized"
fi

echo ""

# Add all files
echo "Adding files to Git..."
git add .
echo "✓ Files added"

echo ""

# Check if there are changes to commit
if [ -n "$(git status --porcelain)" ]; then
    echo "Creating initial commit..."
    git commit -m "Initial commit: Complete DoganSystem implementation

- ABP MVC Application Shell with Entity Framework
- Tenant Management Module
- ERPNext Management Module
- Multi-Agent Orchestrator Module
- Subscription Management Module
- Python Services Integration
- Complete REST API endpoints
- Web Dashboard UI
- Full documentation"
    echo "✓ Initial commit created"
else
    echo "No changes to commit"
fi

echo ""

# Check if remote exists
echo "Checking remote repository..."
if git remote get-url origin &> /dev/null; then
    REMOTE=$(git remote get-url origin)
    echo "✓ Remote already configured: $REMOTE"
    read -p "Update remote? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
        git remote add origin https://github.com/doganlap/DoganSystem.git
        echo "✓ Remote updated"
    fi
else
    echo "Adding remote repository..."
    git remote add origin https://github.com/doganlap/DoganSystem.git
    echo "✓ Remote added: https://github.com/doganlap/DoganSystem.git"
fi

echo ""

# Rename branch to main
echo "Setting branch to main..."
git branch -M main
echo "✓ Branch set to main"

echo ""
echo "==========================================="
echo "Ready to Push!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "2. If authentication is required:"
echo "   - Use Personal Access Token (not password)"
echo "   - Generate at: https://github.com/settings/tokens"
echo ""
echo "3. Or use SSH:"
echo "   git remote set-url origin git@github.com:doganlap/DoganSystem.git"
echo "   git push -u origin main"
echo ""
