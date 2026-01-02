# ERPNext v16 Quick Setup

## Windows Quick Start

### 1. Install Prerequisites (One-time)
- [ ] Python 3.10+ from python.org (check "Add to PATH")
- [ ] Node.js 18+ LTS from nodejs.org
- [ ] MariaDB from mariadb.org
- [ ] Redis (use WSL2 or download Windows version)
- [ ] Git from git-scm.com
- [ ] wkhtmltopdf from wkhtmltopdf.org

### 2. Install Bench
```powershell
pip install frappe-bench
```

### 3. Create ERPNext Instance
```powershell
# Navigate to D:\
cd D:\

# Initialize bench
bench init --frappe-branch version-16 frappe-bench

# Enter bench directory
cd frappe-bench

# Get ERPNext v16
bench get-app erpnext --branch version-16

# Create site
bench new-site mysite.local

# Install ERPNext
bench --site mysite.local install-app erpnext
```

### 4. Start ERPNext
```powershell
bench start
```

Open browser: `http://localhost:8000`

## Linux/macOS Quick Start

### 1. Install Prerequisites
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-dev python3-pip python3-venv nodejs mariadb-server redis-server wkhtmltopdf git

# macOS
brew install python@3.10 node@18 mariadb redis wkhtmltopdf git
```

### 2. Setup
```bash
# Install bench
pip3 install frappe-bench

# Create bench
bench init --frappe-branch version-16 frappe-bench
cd frappe-bench

# Get ERPNext
bench get-app erpnext --branch version-16

# Create site
bench new-site mysite.local

# Install ERPNext
bench --site mysite.local install-app erpnext

# Start
bench start
```

## Server Deployment

```bash
# After local setup, configure for production
bench config production_mode 1
bench setup supervisor
bench setup nginx
bench setup ssl your-domain.com
bench restart
```

## Common Issues

**Port 8000 in use?**
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Database error?**
- Check MariaDB is running
- Verify root password in site_config.json

**Need help?**
- See README.md for detailed instructions
- Check ERPNext docs: https://docs.erpnext.com/
