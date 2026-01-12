#!/bin/bash
# DoganSystem Complete Build and Deploy Script
# Usage: ./deploy-all.sh [local|docker|publish]

set -e

TARGET=${1:-local}
CONFIGURATION=${2:-Release}

echo "========================================"
echo "DoganSystem Build and Deploy"
echo "========================================"
echo "Target: $TARGET"
echo "Configuration: $CONFIGURATION"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check .NET SDK
echo -e "${YELLOW}Checking .NET SDK...${NC}"
if ! command -v dotnet &> /dev/null; then
    echo -e "${RED}ERROR: .NET SDK not found. Please install .NET 8.0 SDK.${NC}"
    exit 1
fi
DOTNET_VERSION=$(dotnet --version)
echo -e "${GREEN}✓ .NET SDK $DOTNET_VERSION found${NC}"
echo ""

# Restore packages
echo -e "${YELLOW}Restoring NuGet packages...${NC}"
dotnet restore DoganSystem.sln
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Package restore failed.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Packages restored${NC}"
echo ""

# Build solution
echo -e "${YELLOW}Building solution ($CONFIGURATION)...${NC}"
dotnet build DoganSystem.sln --configuration $CONFIGURATION --no-restore
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Build failed.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Build successful${NC}"
echo ""

# Publish web application
echo -e "${YELLOW}Publishing web application...${NC}"
PUBLISH_PATH="src/DoganSystem.Web.Mvc/publish"
if [ -d "$PUBLISH_PATH" ]; then
    rm -rf "$PUBLISH_PATH"
fi
dotnet publish "src/DoganSystem.Web.Mvc/DoganSystem.Web.Mvc.csproj" \
    --configuration $CONFIGURATION \
    --output "$PUBLISH_PATH" \
    --no-build
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Publish failed.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Published to: $PUBLISH_PATH${NC}"
echo ""

# Create data directory
mkdir -p data
mkdir -p etc/policies

# Deploy based on target
case $TARGET in
    "local")
        echo -e "${YELLOW}Starting application locally...${NC}"
        cd src/DoganSystem.Web.Mvc
        dotnet run --configuration $CONFIGURATION
        ;;
    "docker")
        echo -e "${YELLOW}Building Docker image...${NC}"
        docker build -t dogansystem:latest .
        if [ $? -ne 0 ]; then
            echo -e "${RED}ERROR: Docker build failed.${NC}"
            exit 1
        fi
        echo -e "${GREEN}✓ Docker image built${NC}"
        echo ""
        echo -e "${YELLOW}Starting Docker container...${NC}"
        docker-compose up -d
        echo -e "${GREEN}✓ Container started${NC}"
        echo ""
        echo -e "${GREEN}Application is running at:${NC}"
        echo -e "  HTTP:  http://localhost:8080"
        echo -e "  HTTPS: https://localhost:8443"
        ;;
    "publish")
        echo -e "${GREEN}✓ Application published to: $PUBLISH_PATH${NC}"
        echo ""
        echo -e "${YELLOW}Next steps:${NC}"
        echo -e "  1. Copy $PUBLISH_PATH to your server"
        echo -e "  2. Configure connection string in appsettings.json"
        echo -e "  3. Run database migrations"
        echo -e "  4. Start the application"
        ;;
    *)
        echo -e "${RED}ERROR: Unknown deployment target: $TARGET${NC}"
        echo -e "${YELLOW}Valid targets: local, docker, publish${NC}"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo -e "${GREEN}Deployment Complete!${NC}"
echo "========================================"
