#!/bin/bash
# Security Fixes Validation Script
# Validates all security fixes applied to the deployment

set -e

echo "=========================================="
echo "Security Fixes Validation"
echo "=========================================="
echo ""

ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    local file=$1
    local pattern=$2
    local description=$3
    local should_exist=${4:-true}
    
    if [ ! -f "$file" ]; then
        if [ "$should_exist" = "true" ]; then
            echo -e "${RED}✗${NC} File not found: $file"
            ((ERRORS++))
        fi
        return
    fi
    
    if grep -q "$pattern" "$file"; then
        echo -e "${RED}✗${NC} $description"
        echo "  Found in: $file"
        ((ERRORS++))
    else
        echo -e "${GREEN}✓${NC} $description"
    fi
}

check_file_contains() {
    local file=$1
    local pattern=$2
    local description=$3
    
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗${NC} File not found: $file"
        ((ERRORS++))
        return
    fi
    
    if grep -q "$pattern" "$file"; then
        echo -e "${GREEN}✓${NC} $description"
    else
        echo -e "${RED}✗${NC} $description"
        echo "  Missing in: $file"
        ((ERRORS++))
    fi
}

echo "1. Checking CORS Configuration..."
echo "-----------------------------------"
for file in agent-setup/api-gateway.py agent-setup/api-server.py agent-setup/webhook-receiver.py \
            agent-setup/tenant-admin-api.py agent-setup/tenant-api.py agent-setup/monitoring-dashboard.py \
            agent-setup/email-api-server.py; do
    check_file "$file" 'allow_origins=\["\*"\]' "CORS wildcard removed in $(basename $file)"
done
echo ""

echo "2. Checking Security Headers..."
echo "-----------------------------------"
check_file_contains "nginx/nginx.production.conf" "Content-Security-Policy" "CSP header added to nginx"
check_file_contains "nginx/nginx.production.conf" "X-Frame-Options" "X-Frame-Options header present"
check_file_contains "nginx/nginx.production.conf" "X-Content-Type-Options" "X-Content-Type-Options header present"
check_file_contains "nginx/nginx.production.conf" "Strict-Transport-Security" "HSTS header present"
echo ""

echo "3. Checking AllowedHosts..."
echo "-----------------------------------"
check_file "src/DoganSystem.Web.Mvc/appsettings.json" '"AllowedHosts": "\*"' "AllowedHosts wildcard removed"
check_file_contains "src/DoganSystem.Web.Mvc/appsettings.json" "doganconsult.com" "AllowedHosts contains doganconsult.com"
echo ""

echo "4. Checking Default Passwords..."
echo "-----------------------------------"
check_file "docker-compose.production.yml" ":-admin123" "Default admin password removed"
check_file "docker-compose.production.yml" ":-erpnext123" "Default ERPNext password removed"
echo ""

echo "5. Checking Placeholder Secrets..."
echo "-----------------------------------"
check_file "src/DoganSystem.Web.Mvc/appsettings.json" "YOUR_SMTP_HOST" "SMTP placeholder removed"
check_file "src/DoganSystem.Web.Mvc/appsettings.json" "YOUR_ERPNEXT_API_KEY" "ERPNext API key placeholder removed"
check_file_contains "src/DoganSystem.Web.Mvc/appsettings.json" "\${SMTP_HOST}" "SMTP uses environment variable"
check_file_contains "src/DoganSystem.Web.Mvc/appsettings.json" "\${ERPNEXT_API_KEY}" "ERPNext uses environment variable"
echo ""

echo "6. Checking Redis Security..."
echo "-----------------------------------"
check_file "docker-compose.production.yml" 'ports:\s*-\s*"6379:6379"' "Redis port mapping removed"
check_file_contains "docker-compose.production.yml" "requirepass" "Redis password authentication enabled"
check_file_contains "docker-compose.production.yml" "REDIS_PASSWORD" "REDIS_PASSWORD environment variable added"
check_file_contains "agent-setup/event-bus.py" "redis_password" "EventBus accepts Redis password"
echo ""

echo "7. Checking Domain Configuration..."
echo "-----------------------------------"
check_file "nginx/nginx.production.conf" "saudibusinessgate.com" "Old domain (saudibusinessgate) removed"
check_file_contains "nginx/nginx.production.conf" "doganconsult.com" "Domain standardized to doganconsult.com"
check_file_contains "src/DoganSystem.Web.Mvc/appsettings.json" "doganconsult.com" "appsettings uses doganconsult.com"
echo ""

echo "8. Checking CORS Environment Variable Support..."
echo "-----------------------------------"
for file in agent-setup/api-gateway.py agent-setup/api-server.py agent-setup/webhook-receiver.py \
            agent-setup/tenant-admin-api.py agent-setup/tenant-api.py agent-setup/monitoring-dashboard.py \
            agent-setup/email-api-server.py; do
    check_file_contains "$file" "CORS_ALLOWED_ORIGINS" "CORS uses environment variable in $(basename $file)"
done
echo ""

echo "=========================================="
echo "Validation Summary"
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All security fixes validated successfully!${NC}"
    exit 0
else
    echo -e "${RED}✗ Found $ERRORS error(s)${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ Found $WARNINGS warning(s)${NC}"
    fi
    exit 1
fi
