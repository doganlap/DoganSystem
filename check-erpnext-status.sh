#!/bin/bash
# Check ERPNext Installation Status
# Run: chmod +x check-erpnext-status.sh && ./check-erpnext-status.sh

echo "==========================================="
echo "ERPNext Installation Status Check"
echo "==========================================="
echo ""

BENCH_INSTALLED=false
BENCH_FOUND=false
ERPNEXT_INSTALLED=false
SITE_CREATED=false
RUNNING=false

# Check if bench CLI is installed
echo "1. Checking Bench CLI..."
if command -v bench &> /dev/null; then
    BENCH_VERSION=$(bench --version 2>&1)
    echo "   ✓ Bench CLI installed: $BENCH_VERSION"
    BENCH_INSTALLED=true
else
    echo "   ✗ Bench CLI not found"
    echo "   → Install with: pip3 install frappe-bench"
fi

# Check for frappe-bench directory
echo ""
echo "2. Checking for Frappe Bench directory..."
POSSIBLE_LOCATIONS=(
    "$HOME/frappe-bench"
    "$HOME/bench"
    "./frappe-bench"
    "./bench"
)

BENCH_PATH=""
for location in "${POSSIBLE_LOCATIONS[@]}"; do
    if [ -d "$location" ]; then
        BENCH_PATH="$location"
        echo "   ✓ Found bench at: $location"
        BENCH_FOUND=true
        break
    fi
done

if [ -z "$BENCH_PATH" ]; then
    echo "   ✗ Frappe Bench directory not found"
    echo "   → Create with: bench init --frappe-branch version-16.2 frappe-bench"
fi

# Check if ERPNext app is installed
if [ -n "$BENCH_PATH" ]; then
    echo ""
    echo "3. Checking ERPNext installation..."
    ERPNEXT_PATH="$BENCH_PATH/apps/erpnext"
    if [ -d "$ERPNEXT_PATH" ]; then
        echo "   ✓ ERPNext app found"
        ERPNEXT_INSTALLED=true
    else
        echo "   ✗ ERPNext app not found"
        echo "   → Install with: bench get-app erpnext --branch version-16.2"
    fi

    # Check for sites
    echo ""
    echo "4. Checking for sites..."
    SITES_PATH="$BENCH_PATH/sites"
    if [ -d "$SITES_PATH" ]; then
        SITES=$(find "$SITES_PATH" -maxdepth 1 -type d ! -path "$SITES_PATH" | wc -l)
        if [ "$SITES" -gt 0 ]; then
            echo "   ✓ Found $SITES site(s):"
            for site in "$SITES_PATH"/*; do
                if [ -d "$site" ]; then
                    echo "     - $(basename "$site")"
                fi
            done
            SITE_CREATED=true
        else
            echo "   ✗ No sites found"
            echo "   → Create with: bench new-site your-site.local"
        fi
    else
        echo "   ✗ Sites directory not found"
    fi
fi

# Check if ERPNext is running
echo ""
echo "5. Checking if ERPNext is running..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200"; then
    echo "   ✓ ERPNext is running on http://localhost:8000"
    RUNNING=true
else
    echo "   ✗ ERPNext is not running"
    echo "   → Start with: bench start"
fi

# Summary
echo ""
echo "==========================================="
echo "Summary"
echo "==========================================="

if [ "$BENCH_INSTALLED" = true ] && [ "$BENCH_FOUND" = true ] && [ "$ERPNEXT_INSTALLED" = true ] && [ "$SITE_CREATED" = true ] && [ "$RUNNING" = true ]; then
    echo "✓ ERPNext is FULLY SETUP and RUNNING!"
elif [ "$BENCH_INSTALLED" = true ] && [ "$BENCH_FOUND" = true ] && [ "$ERPNEXT_INSTALLED" = true ] && [ "$SITE_CREATED" = true ]; then
    echo "⚠ ERPNext is INSTALLED but NOT RUNNING"
    echo "  → Run: bench start"
elif [ "$BENCH_INSTALLED" = true ] && [ "$BENCH_FOUND" = true ]; then
    echo "⚠ ERPNext is PARTIALLY SETUP"
    echo "  → Complete installation steps"
else
    echo "✗ ERPNext is NOT INSTALLED"
    echo "  → Follow installation guide in README.md"
fi

echo ""
