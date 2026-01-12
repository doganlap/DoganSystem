#!/bin/bash
# ERPNext v16.2 Linux Installation Script
# Run: chmod +x install-linux.sh && ./install-linux.sh

set -e

echo "==========================================="
echo "ERPNext v16.2 Installation Script for Linux"
echo "==========================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo "Please do not run this script as root"
   exit 1
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS. Exiting."
    exit 1
fi

echo "Detected OS: $OS"
echo ""

# Update system
echo "Updating system packages..."
if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    sudo apt update
    sudo apt upgrade -y

    # Install prerequisites
    echo "Installing prerequisites..."
    sudo apt install -y python3-dev python3-pip python3-venv python3-setuptools \
        curl git libffi-dev libssl-dev libmysqlclient-dev

    # Install Node.js 18
    echo "Installing Node.js 18..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs

    # Install MariaDB
    echo "Installing MariaDB..."
    sudo apt install -y mariadb-server mariadb-client

    # Install Redis
    echo "Installing Redis..."
    sudo apt install -y redis-server

    # Install wkhtmltopdf
    echo "Installing wkhtmltopdf..."
    sudo apt install -y wkhtmltopdf

elif [ "$OS" = "fedora" ] || [ "$OS" = "rhel" ] || [ "$OS" = "centos" ]; then
    sudo dnf update -y
    sudo dnf install -y python3-devel python3-pip python3-venv nodejs npm \
        mariadb-server mariadb redis git wkhtmltopdf
else
    echo "Unsupported OS. Please install prerequisites manually."
    exit 1
fi

# Verify installations
echo ""
echo "Verifying installations..."
python3 --version
node --version
npm --version
git --version
mysql --version || echo "MariaDB version check skipped"

# Configure MariaDB
echo ""
echo "Configuring MariaDB..."
echo "You will be prompted to set a root password for MariaDB."
read -p "Press Enter to continue with MariaDB setup..."
sudo mysql_secure_installation

# Install bench
echo ""
echo "Installing Frappe Bench CLI..."
pip3 install frappe-bench

# Add to PATH if needed
if ! command -v bench &> /dev/null; then
    echo "Adding bench to PATH..."
    export PATH=$PATH:~/.local/bin
    echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
    source ~/.bashrc
fi

# Verify bench installation
echo ""
echo "Verifying bench installation..."
bench --version || echo "Please restart your terminal or run: source ~/.bashrc"

echo ""
echo "==========================================="
echo "Installation Complete!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. mkdir -p ~/frappe-bench && cd ~/frappe-bench"
echo "2. bench init --frappe-branch version-16.2 frappe-bench"
echo "3. cd frappe-bench"
echo "4. bench get-app erpnext --branch version-16.2"
echo "5. bench new-site your-site-name.local"
echo "6. bench --site your-site-name.local install-app erpnext"
echo "7. bench start"
echo ""
echo "For detailed instructions, see README.md"
