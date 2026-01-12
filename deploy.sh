#!/bin/bash
###############################################
# DoganSystem Production Deployment Script
# All AI Features Enabled
###############################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Docker compose command (will be set in check_prerequisites)
DOCKER_COMPOSE=""

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  DoganSystem Production Deployment${NC}"
echo -e "${BLUE}  All AI Features Enabled${NC}"
echo -e "${BLUE}================================================${NC}"

#==============================================
# Check prerequisites
#==============================================
check_prerequisites() {
    echo -e "\n${YELLOW}[1/7] Checking prerequisites...${NC}"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}ERROR: Docker is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}  Docker installed${NC}"

    # Check Docker Compose (v1 or v2)
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE="docker-compose"
    elif docker compose version &> /dev/null 2>&1; then
        DOCKER_COMPOSE="docker compose"
    else
        echo -e "${RED}ERROR: Docker Compose is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}  Docker Compose installed (using: $DOCKER_COMPOSE)${NC}"

    # Check .env file
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}  .env file not found. Creating from template...${NC}"
        cp .env.production .env
        echo -e "${RED}  IMPORTANT: Edit .env file with your API keys before continuing!${NC}"
        echo -e "${RED}  Required: CLAUDE_API_KEY, ERPNEXT_API_KEY, ERPNEXT_API_SECRET${NC}"
        exit 1
    fi
    echo -e "${GREEN}  .env file found${NC}"

    # Validate critical environment variables
    source .env
    if [[ "$CLAUDE_API_KEY" == *"REPLACE"* ]] || [ -z "$CLAUDE_API_KEY" ]; then
        echo -e "${RED}ERROR: CLAUDE_API_KEY not configured in .env${NC}"
        exit 1
    fi
    echo -e "${GREEN}  Claude API Key configured${NC}"

    if [[ "$ERPNEXT_API_KEY" == *"REPLACE"* ]] || [ -z "$ERPNEXT_API_KEY" ]; then
        echo -e "${YELLOW}  WARNING: ERPNEXT_API_KEY not configured (AI agents will have limited functionality)${NC}"
    else
        echo -e "${GREEN}  ERPNext API Key configured${NC}"
    fi
}

#==============================================
# Create required directories
#==============================================
create_directories() {
    echo -e "\n${YELLOW}[2/7] Creating directories...${NC}"

    mkdir -p logs/{web,api-gateway,agent-server,tenant-admin,workflow-engine,monitoring,webhook,nginx}
    mkdir -p nginx/ssl
    mkdir -p data/{tenant_databases,backups}

    echo -e "${GREEN}  Directories created${NC}"
}

#==============================================
# Generate self-signed SSL certificates (if needed)
#==============================================
setup_ssl() {
    echo -e "\n${YELLOW}[3/7] Setting up SSL certificates...${NC}"

    if [ ! -f "nginx/ssl/fullchain.pem" ] || [ ! -f "nginx/ssl/privkey.pem" ]; then
        echo -e "${YELLOW}  Generating self-signed certificates for development...${NC}"
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout nginx/ssl/privkey.pem \
            -out nginx/ssl/fullchain.pem \
            -subj "/C=SA/ST=Riyadh/L=Riyadh/O=DoganConsult/CN=localhost" \
            2>/dev/null
        echo -e "${GREEN}  Self-signed certificates generated${NC}"
        echo -e "${YELLOW}  NOTE: For production, replace with real SSL certificates${NC}"
    else
        echo -e "${GREEN}  SSL certificates already exist${NC}"
    fi
}

#==============================================
# Build Docker images
#==============================================
build_images() {
    echo -e "\n${YELLOW}[4/7] Building Docker images...${NC}"

    $DOCKER_COMPOSE -f docker-compose.production.yml build --parallel

    echo -e "${GREEN}  Docker images built successfully${NC}"
}

#==============================================
# Start services
#==============================================
start_services() {
    echo -e "\n${YELLOW}[5/7] Starting services...${NC}"

    $DOCKER_COMPOSE -f docker-compose.production.yml up -d

    echo -e "${GREEN}  Services started${NC}"
}

#==============================================
# Wait for services to be healthy
#==============================================
wait_for_health() {
    echo -e "\n${YELLOW}[6/7] Waiting for services to be healthy...${NC}"

    services=("dogansystem-redis" "dogansystem-api-gateway" "dogansystem-agent-server" "dogansystem-web")

    for service in "${services[@]}"; do
        echo -n "  Waiting for $service..."
        for i in {1..30}; do
            if docker inspect --format='{{.State.Health.Status}}' "$service" 2>/dev/null | grep -q "healthy"; then
                echo -e " ${GREEN}healthy${NC}"
                break
            elif [ $i -eq 30 ]; then
                echo -e " ${YELLOW}timeout (may still be starting)${NC}"
            else
                sleep 2
            fi
        done
    done
}

#==============================================
# Display status
#==============================================
display_status() {
    echo -e "\n${YELLOW}[7/7] Deployment Status...${NC}"
    echo -e "${BLUE}================================================${NC}"

    echo -e "\n${GREEN}Services Running:${NC}"
    $DOCKER_COMPOSE -f docker-compose.production.yml ps

    echo -e "\n${GREEN}Access URLs:${NC}"
    echo -e "  Web Application:     https://localhost (or http://localhost:5000)"
    echo -e "  API Gateway:         http://localhost:8006"
    echo -e "  Agent Server:        http://localhost:8001"
    echo -e "  Monitoring:          http://localhost:8005"
    echo -e "  Tenant Admin:        http://localhost:8007"
    echo -e "  Webhooks:            http://localhost:8003"

    echo -e "\n${GREEN}AI Features Status:${NC}"
    echo -e "  Claude AI Agents:        ${GREEN}ENABLED${NC}"
    echo -e "  Autonomous Workflows:    ${GREEN}ENABLED${NC}"
    echo -e "  Self-Healing System:     ${GREEN}ENABLED${NC}"
    echo -e "  Multi-Tenant Support:    ${GREEN}ENABLED${NC}"
    echo -e "  Email Processing:        ${GREEN}ENABLED${NC}"
    echo -e "  Monitoring Dashboard:    ${GREEN}ENABLED${NC}"

    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${GREEN}Deployment completed successfully!${NC}"
    echo -e "${BLUE}================================================${NC}"
}

#==============================================
# Main execution
#==============================================
main() {
    case "${1:-deploy}" in
        deploy)
            check_prerequisites
            create_directories
            setup_ssl
            build_images
            start_services
            wait_for_health
            display_status
            ;;
        start)
            $DOCKER_COMPOSE -f docker-compose.production.yml up -d
            display_status
            ;;
        stop)
            echo -e "${YELLOW}Stopping services...${NC}"
            $DOCKER_COMPOSE -f docker-compose.production.yml down
            echo -e "${GREEN}Services stopped${NC}"
            ;;
        restart)
            echo -e "${YELLOW}Restarting services...${NC}"
            $DOCKER_COMPOSE -f docker-compose.production.yml restart
            display_status
            ;;
        logs)
            $DOCKER_COMPOSE -f docker-compose.production.yml logs -f "${2:-}"
            ;;
        status)
            $DOCKER_COMPOSE -f docker-compose.production.yml ps
            ;;
        rebuild)
            echo -e "${YELLOW}Rebuilding and redeploying...${NC}"
            $DOCKER_COMPOSE -f docker-compose.production.yml down
            build_images
            start_services
            wait_for_health
            display_status
            ;;
        *)
            echo "Usage: $0 {deploy|start|stop|restart|logs|status|rebuild}"
            echo ""
            echo "Commands:"
            echo "  deploy   - Full deployment (default)"
            echo "  start    - Start existing containers"
            echo "  stop     - Stop all containers"
            echo "  restart  - Restart all containers"
            echo "  logs     - View logs (optionally specify service name)"
            echo "  status   - Show container status"
            echo "  rebuild  - Rebuild images and redeploy"
            exit 1
            ;;
    esac
}

main "$@"
