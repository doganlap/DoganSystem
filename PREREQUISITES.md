# ERPNext v16.2 Prerequisites Checklist

Use this checklist to ensure all prerequisites are installed before setting up ERPNext v16.2.

## Required Software

### Windows
- [ ] **Python 3.10+**
  - Download: https://www.python.org/downloads/
  - Version check: `python --version`
  - ⚠️ Important: Check "Add Python to PATH" during installation

- [ ] **Node.js 18+ (LTS)**
  - Download: https://nodejs.org/
  - Version check: `node --version` and `npm --version`

- [ ] **MariaDB 10.6+**
  - Download: https://mariadb.org/download/
  - Set root password during installation
  - Verify: `mysql --version`

- [ ] **Redis**
  - Option 1: Use WSL2 (recommended)
    ```powershell
    wsl sudo apt-get install redis-server
    ```
  - Option 2: Download Windows version from GitHub
  - Verify: `redis-cli ping` (should return "PONG")

- [ ] **Git**
  - Download: https://git-scm.com/download/win
  - Verify: `git --version`

- [ ] **wkhtmltopdf**
  - Download: https://wkhtmltopdf.org/downloads.html
  - Add to system PATH
  - Verify: `wkhtmltopdf --version`

- [ ] **pip** (usually comes with Python)
  - Verify: `pip --version`
  - If missing: `python -m ensurepip --upgrade`

### Linux (Ubuntu/Debian)
- [ ] **Python 3.10+**
  ```bash
  python3 --version
  sudo apt install python3-dev python3-pip python3-venv
  ```

- [ ] **Node.js 18+**
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
  sudo apt install -y nodejs
  node --version
  ```

- [ ] **MariaDB 10.6+**
  ```bash
  sudo apt install mariadb-server mariadb-client
  sudo mysql_secure_installation
  ```

- [ ] **Redis**
  ```bash
  sudo apt install redis-server
  sudo systemctl start redis
  redis-cli ping
  ```

- [ ] **Git**
  ```bash
  sudo apt install git
  git --version
  ```

- [ ] **wkhtmltopdf**
  ```bash
  sudo apt install wkhtmltopdf
  wkhtmltopdf --version
  ```

- [ ] **Additional dependencies**
  ```bash
  sudo apt install libffi-dev libssl-dev libmysqlclient-dev
  ```

### macOS
- [ ] **Homebrew** (if not installed)
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

- [ ] **Python 3.10+**
  ```bash
  brew install python@3.10
  python3 --version
  ```

- [ ] **Node.js 18+**
  ```bash
  brew install node@18
  node --version
  ```

- [ ] **MariaDB**
  ```bash
  brew install mariadb
  brew services start mariadb
  ```

- [ ] **Redis**
  ```bash
  brew install redis
  brew services start redis
  redis-cli ping
  ```

- [ ] **Git** (usually pre-installed)
  ```bash
  git --version
  ```

- [ ] **wkhtmltopdf**
  ```bash
  brew install wkhtmltopdf
  ```

## System Requirements

- [ ] **RAM**: Minimum 4GB (8GB+ recommended)
- [ ] **Storage**: At least 20GB free space
- [ ] **OS**: 
  - Windows 10/11 (WSL2 recommended)
  - Ubuntu 20.04/22.04 LTS
  - macOS 11+
  - Other Linux distributions (with manual setup)

## Verification Commands

Run these commands to verify all prerequisites:

```bash
# Python
python --version  # or python3 --version
pip --version     # or pip3 --version

# Node.js
node --version
npm --version

# Database
mysql --version   # or mariadb --version

# Redis
redis-cli ping    # Should return "PONG"

# Git
git --version

# wkhtmltopdf
wkhtmltopdf --version
```

## Next Steps

Once all prerequisites are checked:
1. Install Bench CLI: `pip install frappe-bench` (or `pip3 install frappe-bench`)
2. Follow the setup instructions in README.md
3. Or run the installation script:
   - Windows: `.\install-windows.ps1` (as Administrator)
   - Linux: `chmod +x install-linux.sh && ./install-linux.sh`

## Troubleshooting

### Python not found
- Windows: Reinstall Python and check "Add to PATH"
- Linux/Mac: Use `python3` instead of `python`

### pip not found
```bash
python -m ensurepip --upgrade
# or
python3 -m ensurepip --upgrade
```

### Node.js version too old
- Uninstall old version
- Install Node.js 18+ LTS from nodejs.org

### MariaDB connection issues
- Verify service is running: `sudo systemctl status mariadb` (Linux)
- Check root password
- Verify port 3306 is not blocked

### Redis connection issues
- Start Redis service: `sudo systemctl start redis` (Linux)
- Windows: Use WSL2 or ensure Redis service is running
