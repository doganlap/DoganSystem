###############################################
# DoganSystem Production Dockerfile
# Multi-stage build for optimized image
###############################################

# Stage 1: Base runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 5000

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj files and restore dependencies
COPY ["src/DoganSystem.Web.Mvc/DoganSystem.Web.Mvc.csproj", "src/DoganSystem.Web.Mvc/"]
COPY ["src/DoganSystem.Application/DoganSystem.Application.csproj", "src/DoganSystem.Application/"]
COPY ["src/DoganSystem.Core/DoganSystem.Core.csproj", "src/DoganSystem.Core/"]
COPY ["src/DoganSystem.EntityFrameworkCore/DoganSystem.EntityFrameworkCore.csproj", "src/DoganSystem.EntityFrameworkCore/"]
COPY ["src/DoganSystem.Modules.ErpNext/DoganSystem.Modules.ErpNext.csproj", "src/DoganSystem.Modules.ErpNext/"]
COPY ["src/DoganSystem.Modules.TenantManagement/DoganSystem.Modules.TenantManagement.csproj", "src/DoganSystem.Modules.TenantManagement/"]
COPY ["src/DoganSystem.Modules.AgentOrchestrator/DoganSystem.Modules.AgentOrchestrator.csproj", "src/DoganSystem.Modules.AgentOrchestrator/"]
COPY ["src/DoganSystem.Modules.Subscription/DoganSystem.Modules.Subscription.csproj", "src/DoganSystem.Modules.Subscription/"]

RUN dotnet restore "src/DoganSystem.Web.Mvc/DoganSystem.Web.Mvc.csproj"

# Copy everything else and build
COPY . .
WORKDIR "/src/src/DoganSystem.Web.Mvc"
RUN dotnet build "DoganSystem.Web.Mvc.csproj" -c Release -o /app/build

# Stage 3: Publish
FROM build AS publish
RUN dotnet publish "DoganSystem.Web.Mvc.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Stage 4: Final production image
FROM base AS final
WORKDIR /app

# Create non-root user for security
RUN useradd -m -s /bin/bash appuser

# Create directories
RUN mkdir -p /app/data /app/logs && chown -R appuser:appuser /app

# Copy published application
COPY --from=publish /app/publish .
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Environment variables
ENV ASPNETCORE_URLS=http://+:5000
ENV ASPNETCORE_ENVIRONMENT=Production
ENV DOTNET_RUNNING_IN_CONTAINER=true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

ENTRYPOINT ["dotnet", "DoganSystem.Web.Mvc.dll"]
