#!/bin/bash
###############################################
# DoganSystem Docker Build and Push Script
# Builds and pushes images to Docker Hub
###############################################

set -e

# Configuration
DOCKER_USERNAME=${DOCKER_USERNAME:-doganlap}
VERSION=${1:-latest}
PUSH=${2:-true}  # Set to 'false' to skip push

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  DoganSystem Docker Build and Push${NC}"
echo -e "${BLUE}================================================${NC}"
echo -e "Docker Hub: ${DOCKER_USERNAME}"
echo -e "Version: ${VERSION}"
echo -e "Push: ${PUSH}"
echo ""

# Check if logged in to Docker Hub
echo -e "${YELLOW}Checking Docker Hub authentication...${NC}"
if ! docker info | grep -q "Username: ${DOCKER_USERNAME}"; then
    echo -e "${YELLOW}Not logged in to Docker Hub. Attempting login...${NC}"
    if [ -z "$DOCKER_PASSWORD" ]; then
        echo -e "${RED}ERROR: DOCKER_PASSWORD environment variable not set${NC}"
        echo -e "${YELLOW}Please set DOCKER_PASSWORD or run: docker login -u ${DOCKER_USERNAME}${NC}"
        exit 1
    fi
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
fi
echo -e "${GREEN}✓ Authenticated as ${DOCKER_USERNAME}${NC}"
echo ""

# Build and tag web application
echo -e "${YELLOW}[1/2] Building dogansystem-web...${NC}"
docker build -t ${DOCKER_USERNAME}/dogansystem-web:${VERSION} -f Dockerfile .
docker tag ${DOCKER_USERNAME}/dogansystem-web:${VERSION} ${DOCKER_USERNAME}/dogansystem-web:latest
echo -e "${GREEN}✓ Web application image built${NC}"
echo ""

# Build and tag AI services
echo -e "${YELLOW}[2/2] Building dogansystem-ai...${NC}"
docker build -t ${DOCKER_USERNAME}/dogansystem-ai:${VERSION} -f agent-setup/Dockerfile ./agent-setup
docker tag ${DOCKER_USERNAME}/dogansystem-ai:${VERSION} ${DOCKER_USERNAME}/dogansystem-ai:latest
echo -e "${GREEN}✓ AI services image built${NC}"
echo ""

# Push images if requested
if [ "$PUSH" = "true" ]; then
    echo -e "${YELLOW}Pushing images to Docker Hub...${NC}"
    
    echo -e "  Pushing ${DOCKER_USERNAME}/dogansystem-web:${VERSION}..."
    docker push ${DOCKER_USERNAME}/dogansystem-web:${VERSION}
    
    echo -e "  Pushing ${DOCKER_USERNAME}/dogansystem-web:latest..."
    docker push ${DOCKER_USERNAME}/dogansystem-web:latest
    
    echo -e "  Pushing ${DOCKER_USERNAME}/dogansystem-ai:${VERSION}..."
    docker push ${DOCKER_USERNAME}/dogansystem-ai:${VERSION}
    
    echo -e "  Pushing ${DOCKER_USERNAME}/dogansystem-ai:latest..."
    docker push ${DOCKER_USERNAME}/dogansystem-ai:latest
    
    echo -e "${GREEN}✓ All images pushed successfully!${NC}"
else
    echo -e "${YELLOW}Skipping push (PUSH=false)${NC}"
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  Build Complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "Images available:"
echo "  - ${DOCKER_USERNAME}/dogansystem-web:${VERSION}"
echo "  - ${DOCKER_USERNAME}/dogansystem-web:latest"
echo "  - ${DOCKER_USERNAME}/dogansystem-ai:${VERSION}"
echo "  - ${DOCKER_USERNAME}/dogansystem-ai:latest"
echo ""
if [ "$PUSH" = "true" ]; then
    echo "View on Docker Hub:"
    echo "  https://hub.docker.com/r/${DOCKER_USERNAME}/dogansystem-web"
    echo "  https://hub.docker.com/r/${DOCKER_USERNAME}/dogansystem-ai"
fi
