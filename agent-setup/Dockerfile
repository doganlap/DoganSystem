# Multi-Tenant SaaS Platform Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p tenant_databases logs backups

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PLATFORM_DB_PATH=/app/data/platform.db
ENV TENANT_DB_DIR=/app/data/tenant_databases

# Expose ports
EXPOSE 8002 8003 8005 8006 8007

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8002/')" || exit 1

# Default command (can be overridden)
CMD ["python", "api-gateway.py"]
