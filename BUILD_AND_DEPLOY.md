# Build and Deploy Guide - DoganSystem

## 🚀 Quick Start: Build and Run

### Prerequisites
- ✅ .NET 8.0 SDK installed
- ✅ SQL Server (Express, LocalDB, or full SQL Server)
- ✅ Visual Studio 2022, VS Code, or any .NET IDE

### Step 1: Restore Dependencies
```bash
cd D:\DoganSystem
dotnet restore
```

### Step 2: Build the Solution
```bash
dotnet build DoganSystem.sln --configuration Release
```

### Step 3: Configure Database Connection
Edit `src/DoganSystem.Web.Mvc/appsettings.json`:
```json
{
  "ConnectionStrings": {
    "Default": "Server=localhost;Database=DoganSystemDb;Trusted_Connection=True;TrustServerCertificate=True"
  }
}
```

**For SQL Server Express:**
```json
"Default": "Server=localhost\\SQLEXPRESS;Database=DoganSystemDb;Trusted_Connection=True;TrustServerCertificate=True"
```

**For SQL Server with credentials:**
```json
"Default": "Server=your-server;Database=DoganSystemDb;User Id=your-user;Password=your-password;TrustServerCertificate=True"
```

### Step 4: Create Database Migration
```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial --startup-project ../DoganSystem.Web.Mvc
dotnet ef database update --startup-project ../DoganSystem.Web.Mvc
```

**Note:** If you don't have EF Core tools installed:
```bash
dotnet tool install --global dotnet-ef
```

### Step 5: Run the Application
```bash
cd src/DoganSystem.Web.Mvc
dotnet run
```

The application will start at:
- **Web UI:** http://localhost:5000
- **HTTPS:** https://localhost:5001
- **API Docs:** http://localhost:5000/swagger (Development only)

---

## 📦 Build for Production

### Build Release Version
```bash
dotnet build DoganSystem.sln --configuration Release
```

### Publish for Deployment
```bash
cd src/DoganSystem.Web.Mvc
dotnet publish --configuration Release --output ./publish
```

This creates a publishable package in `src/DoganSystem.Web.Mvc/publish/`

---

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["DoganSystem.sln", "./"]
COPY ["src/DoganSystem.Web.Mvc/DoganSystem.Web.Mvc.csproj", "src/DoganSystem.Web.Mvc/"]
COPY ["src/DoganSystem.Application/DoganSystem.Application.csproj", "src/DoganSystem.Application/"]
COPY ["src/DoganSystem.Core/DoganSystem.Core.csproj", "src/DoganSystem.Core/"]
COPY ["src/DoganSystem.EntityFrameworkCore/DoganSystem.EntityFrameworkCore.csproj", "src/DoganSystem.EntityFrameworkCore/"]
# Add all other project references
RUN dotnet restore "DoganSystem.sln"
COPY . .
WORKDIR "/src/src/DoganSystem.Web.Mvc"
RUN dotnet build "DoganSystem.Web.Mvc.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "DoganSystem.Web.Mvc.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "DoganSystem.Web.Mvc.dll"]
```

### Build Docker Image
```bash
docker build -t dogansystem:latest .
```

### Run Docker Container
```bash
docker run -d -p 8080:80 \
  -e ConnectionStrings__Default="Server=your-sql-server;Database=DoganSystemDb;User Id=sa;Password=your-password;TrustServerCertificate=True" \
  --name dogansystem \
  dogansystem:latest
```

---

## 🌐 IIS Deployment (Windows Server)

### 1. Install Prerequisites
- .NET 8.0 Hosting Bundle: https://dotnet.microsoft.com/download/dotnet/8.0
- ASP.NET Core Runtime 8.0

### 2. Publish Application
```bash
cd src/DoganSystem.Web.Mvc
dotnet publish --configuration Release --output C:\inetpub\wwwroot\DoganSystem
```

### 3. Configure IIS
1. Open IIS Manager
2. Create new Application Pool:
   - Name: `DoganSystemAppPool`
   - .NET CLR Version: **No Managed Code**
   - Managed Pipeline Mode: **Integrated**

3. Create new Website:
   - Physical Path: `C:\inetpub\wwwroot\DoganSystem`
   - Binding: Port 80 (or your preferred port)
   - Application Pool: `DoganSystemAppPool`

4. Update `web.config` (auto-generated) with connection string:
```xml
<configuration>
  <connectionStrings>
    <add name="Default" connectionString="Server=your-server;Database=DoganSystemDb;..." />
  </connectionStrings>
</configuration>
```

---

## ☁️ Azure App Service Deployment

### 1. Create Azure App Service
```bash
az webapp create --resource-group YourResourceGroup --plan YourAppServicePlan --name DoganSystem --runtime "DOTNET|8.0"
```

### 2. Configure Connection String
```bash
az webapp config connection-string set \
  --resource-group YourResourceGroup \
  --name DoganSystem \
  --connection-string-type SQLServer \
  --settings Default="Server=your-azure-sql.database.windows.net;Database=DoganSystemDb;User Id=your-user;Password=your-password"
```

### 3. Deploy from Local
```bash
cd src/DoganSystem.Web.Mvc
dotnet publish --configuration Release
az webapp deploy --resource-group YourResourceGroup --name DoganSystem --src-path ./bin/Release/net8.0/publish
```

### 4. Deploy from GitHub (CI/CD)
1. Push code to GitHub
2. In Azure Portal → App Service → Deployment Center
3. Connect to GitHub repository
4. Configure build settings (auto-detected for .NET)

---

## 🐧 Linux Deployment (Ubuntu/CentOS)

### 1. Install .NET 8.0 Runtime
```bash
# Ubuntu
wget https://dot.net/v1/dotnet-install.sh
chmod +x dotnet-install.sh
./dotnet-install.sh --version 8.0.0

# Add to PATH
export PATH=$PATH:$HOME/.dotnet
```

### 2. Install SQL Server Client
```bash
# Ubuntu
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

### 3. Publish and Deploy
```bash
cd src/DoganSystem.Web.Mvc
dotnet publish --configuration Release --output /var/www/dogansystem
```

### 4. Create Systemd Service
Create `/etc/systemd/system/dogansystem.service`:
```ini
[Unit]
Description=DoganSystem Web Application
After=network.target

[Service]
Type=notify
ExecStart=/usr/bin/dotnet /var/www/dogansystem/DoganSystem.Web.Mvc.dll
Restart=always
RestartSec=10
KillSignal=SIGINT
SyslogIdentifier=dogansystem
User=www-data
Environment=ASPNETCORE_ENVIRONMENT=Production
Environment=ConnectionStrings__Default="Server=your-server;Database=DoganSystemDb;..."

[Install]
WantedBy=multi-user.target
```

### 5. Start Service
```bash
sudo systemctl enable dogansystem
sudo systemctl start dogansystem
sudo systemctl status dogansystem
```

### 6. Configure Nginx (Reverse Proxy)
Create `/etc/nginx/sites-available/dogansystem`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection keep-alive;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/dogansystem /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔧 Environment-Specific Configuration

### Development
- Uses `appsettings.Development.json`
- Swagger enabled
- Detailed error pages
- Hot reload enabled

### Production
- Uses `appsettings.Production.json`
- Swagger disabled
- Error pages simplified
- Logging to files

### Set Environment Variable
```bash
# Windows
set ASPNETCORE_ENVIRONMENT=Production

# Linux/Mac
export ASPNETCORE_ENVIRONMENT=Production
```

---

## ✅ Pre-Deployment Checklist

- [ ] Database connection string configured
- [ ] Database migrations run
- [ ] Environment variables set
- [ ] Production appsettings configured
- [ ] SSL certificate configured (for HTTPS)
- [ ] Firewall rules configured
- [ ] Backup strategy in place
- [ ] Monitoring/logging configured

---

## 🧪 Verify Deployment

### Health Check
```bash
curl http://your-server/api/health
```

### Test API
```bash
curl http://your-server/api/tenants
```

### Check Logs
```bash
# Windows (IIS)
Get-Content C:\inetpub\wwwroot\DoganSystem\Logs\*.txt -Tail 50

# Linux (Systemd)
sudo journalctl -u dogansystem -f
```

---

## 🆘 Troubleshooting

### Build Errors
```bash
# Clean and rebuild
dotnet clean
dotnet restore
dotnet build
```

### Database Connection Issues
- Verify SQL Server is running
- Check firewall rules
- Verify connection string format
- Test connection with SQL Server Management Studio

### Runtime Errors
- Check application logs
- Verify environment variables
- Ensure all dependencies are installed
- Check file permissions (Linux)

---

## 📞 Support

For deployment issues:
1. Check application logs
2. Verify configuration files
3. Test database connectivity
4. Review ABP Framework documentation: https://docs.abp.io/

---

**Ready to Deploy!** 🚀
