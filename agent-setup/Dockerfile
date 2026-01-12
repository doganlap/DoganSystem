###############################################
# DoganSystem AI Services - Production Dockerfile
# Claude AI Agents & Autonomous Workflows
###############################################

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -s /bin/bash aiuser

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories with proper permissions
RUN mkdir -p /app/data/tenant_databases /app/logs /app/backups \
    && chown -R aiuser:aiuser /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PLATFORM_DB_PATH=/app/data/platform.db
ENV TENANT_DB_DIR=/app/data/tenant_databases
ENV LOG_LEVEL=INFO

# Switch to non-root user
USER aiuser

# Expose ports for all services
# 8001 - Agent API Server
# 8003 - Webhook Receiver
# 8005 - Monitoring Dashboard
# 8006 - API Gateway (main)
# 8007 - Tenant Admin API
EXPOSE 8001 8003 8005 8006 8007

# Health check (will be overridden per service)
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8006/health || exit 1

# Default command (override in docker-compose)
CMD ["uvicorn", "api-gateway:app", "--host", "0.0.0.0", "--port", "8006"]
