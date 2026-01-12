# Docker Hub Configuration Guide

## ✅ Docker Hub Authentication Configured

Your Docker Hub credentials have been configured:
- **Username:** `doganlap`
- **Token:** Configured (stored securely in `~/.docker/config.json`)
- **Permissions:** Read, Write, Delete
- **Expires:** Never

## 🔐 Secure Credential Storage

### Current Status
Docker credentials are stored in `~/.docker/config.json`. For enhanced security, consider using Docker credential helpers:

```bash
# Install Docker credential helper (optional, for enhanced security)
# For pass (password store)
docker-credential-pass version

# For osxkeychain (macOS)
docker-credential-osxkeychain version

# Configure credential helper
echo '{"credsStore":"osxkeychain"}' > ~/.docker/config.json
```

### For Production Servers
On production servers, you can use environment variables or Docker secrets:

```bash
# Option 1: Environment variables (for CI/CD)
export DOCKER_USERNAME=doganlap
export DOCKER_PASSWORD=YOUR_DOCKER_HUB_TOKEN

# Option 2: Login directly (credentials stored in ~/.docker/config.json)
echo "YOUR_DOCKER_HUB_TOKEN" | docker login -u doganlap --password-stdin
```

## 🐳 Building and Pushing Images

### Build Images Locally

```bash
# Build C# Web Application
docker build -t doganlap/dogansystem-web:latest -f Dockerfile .

# Build Python AI Services
docker build -t doganlap/dogansystem-ai:latest -f agent-setup/Dockerfile ./agent-setup
```

### Tag Images for Docker Hub

```bash
# Tag with version
docker tag doganlap/dogansystem-web:latest doganlap/dogansystem-web:v1.0.0
docker tag doganlap/dogansystem-ai:latest doganlap/dogansystem-ai:v1.0.0
```

### Push to Docker Hub

```bash
# Push images
docker push doganlap/dogansystem-web:latest
docker push doganlap/dogansystem-web:v1.0.0
docker push doganlap/dogansystem-ai:latest
docker push doganlap/dogansystem-ai:v1.0.0
```

## 📦 Using Docker Hub Images in Production

### Update docker-compose.production.yml

You can use Docker Hub images instead of building locally:

```yaml
services:
  dogansystem-web:
    image: doganlap/dogansystem-web:latest
    # Remove build section if using pre-built images
    # build:
    #   context: .
    #   dockerfile: Dockerfile

  api-gateway:
    image: doganlap/dogansystem-ai:latest
    # Remove build section if using pre-built images
```

### Pull Images on Production Server

```bash
# Login to Docker Hub
docker login -u doganlap

# Pull images
docker-compose -f docker-compose.production.yml pull

# Start services
docker-compose -f docker-compose.production.yml up -d
```

## 🔄 Automated Build and Push Script

Create a script to automate building and pushing:

```bash
#!/bin/bash
# build-and-push.sh

set -e

VERSION=${1:-latest}
DOCKER_USERNAME=doganlap

echo "Building and pushing DoganSystem images..."

# Build and push web application
echo "Building dogansystem-web..."
docker build -t $DOCKER_USERNAME/dogansystem-web:$VERSION -f Dockerfile .
docker tag $DOCKER_USERNAME/dogansystem-web:$VERSION $DOCKER_USERNAME/dogansystem-web:latest
docker push $DOCKER_USERNAME/dogansystem-web:$VERSION
docker push $DOCKER_USERNAME/dogansystem-web:latest

# Build and push AI services
echo "Building dogansystem-ai..."
docker build -t $DOCKER_USERNAME/dogansystem-ai:$VERSION -f agent-setup/Dockerfile ./agent-setup
docker tag $DOCKER_USERNAME/dogansystem-ai:$VERSION $DOCKER_USERNAME/dogansystem-ai:latest
docker push $DOCKER_USERNAME/dogansystem-ai:$VERSION
docker push $DOCKER_USERNAME/dogansystem-ai:latest

echo "✓ All images built and pushed successfully!"
```

## 🚨 Security Best Practices

### ⚠️ NEVER Commit Credentials

- **DO NOT** commit `~/.docker/config.json` to version control
- **DO NOT** hardcode tokens in scripts or configuration files
- **DO** use environment variables or Docker credential helpers
- **DO** add `.docker/config.json` to `.gitignore` (if not already)

### Environment Variables for CI/CD

For GitHub Actions, GitLab CI, or other CI/CD systems:

```yaml
# Example GitHub Actions
env:
  DOCKER_USERNAME: doganlap
  DOCKER_PASSWORD: ${{ secrets.DOCKER_HUB_TOKEN }}

steps:
  - name: Login to Docker Hub
    run: echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
```

### Token Management

- **Rotate tokens regularly** (every 90 days recommended)
- **Use separate tokens** for different environments (dev, staging, prod)
- **Revoke tokens** immediately if compromised
- **Monitor token usage** in Docker Hub dashboard

## 📋 Quick Reference

```bash
# Login
docker login -u doganlap

# Check login status
docker info | grep Username

# Logout (if needed)
docker logout

# Build image
docker build -t doganlap/dogansystem-web:latest .

# Push image
docker push doganlap/dogansystem-web:latest

# Pull image
docker pull doganlap/dogansystem-web:latest
```

## 🔍 Verify Configuration

```bash
# Check if logged in
docker info | grep Username

# Test push (use a test image first)
docker tag hello-world:latest doganlap/test-image:latest
docker push doganlap/test-image:latest
docker rmi doganlap/test-image:latest  # Clean up
```

---

**Status:** ✅ Docker Hub authentication configured and ready to use.
