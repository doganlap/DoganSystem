#!/bin/bash
# DoganSystem Build Script for Linux/Mac
# Usage: ./build.sh [Release|Debug]

CONFIGURATION=${1:-Release}

echo "========================================"
echo "DoganSystem Build Script"
echo "========================================"
echo ""

# Check .NET SDK
echo "Checking .NET SDK..."
if ! command -v dotnet &> /dev/null; then
    echo "ERROR: .NET SDK not found. Please install .NET 8.0 SDK."
    exit 1
fi
DOTNET_VERSION=$(dotnet --version)
echo "✓ .NET SDK $DOTNET_VERSION found"
echo ""

# Restore packages
echo "Restoring NuGet packages..."
dotnet restore DoganSystem.sln
if [ $? -ne 0 ]; then
    echo "ERROR: Package restore failed."
    exit 1
fi
echo "✓ Packages restored"
echo ""

# Build solution
echo "Building solution ($CONFIGURATION)..."
dotnet build DoganSystem.sln --configuration $CONFIGURATION --no-restore
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed."
    exit 1
fi
echo "✓ Build successful"
echo ""

# Publish web application
echo "Publishing web application..."
PUBLISH_PATH="src/DoganSystem.Web.Mvc/publish"
if [ -d "$PUBLISH_PATH" ]; then
    rm -rf "$PUBLISH_PATH"
fi
dotnet publish "src/DoganSystem.Web.Mvc/DoganSystem.Web.Mvc.csproj" \
    --configuration $CONFIGURATION \
    --output "$PUBLISH_PATH" \
    --no-build
if [ $? -ne 0 ]; then
    echo "ERROR: Publish failed."
    exit 1
fi
echo "✓ Published to: $PUBLISH_PATH"
echo ""

echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Update connection string in appsettings.json"
echo "2. Run database migrations:"
echo "   cd src/DoganSystem.EntityFrameworkCore"
echo "   dotnet ef migrations add Initial --startup-project ../DoganSystem.Web.Mvc"
echo "   dotnet ef database update --startup-project ../DoganSystem.Web.Mvc"
echo "3. Run the application:"
echo "   cd src/DoganSystem.Web.Mvc"
echo "   dotnet run"
echo ""
