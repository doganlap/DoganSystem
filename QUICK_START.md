# 🚀 Quick Start - Build and Deploy DoganSystem

## ⚡ Fastest Way to Get Running (5 Minutes)

### Step 1: Build the Application
```powershell
# Windows
.\build.ps1

# OR manually:
dotnet restore
dotnet build DoganSystem.sln --configuration Release
```

### Step 2: Configure Database
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

### Step 3: Create Database
```powershell
# Install EF Core tools (if not installed)
dotnet tool install --global dotnet-ef

# Create and apply migrations
cd src\DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial --startup-project ..\DoganSystem.Web.Mvc
dotnet ef database update --startup-project ..\DoganSystem.Web.Mvc
```

### Step 4: Run the Application
```powershell
cd src\DoganSystem.Web.Mvc
dotnet run
```

### Step 5: Access the Application
- **Web UI:** http://localhost:5000
- **API Docs:** http://localhost:5000/swagger

---

## 📦 Build for Production

### Option 1: Using Build Script
```powershell
.\build.ps1 Release
```

### Option 2: Manual Build
```powershell
dotnet build DoganSystem.sln --configuration Release
dotnet publish src\DoganSystem.Web.Mvc\DoganSystem.Web.Mvc.csproj --configuration Release --output ./publish
```

---

## 🐳 Docker Deployment

### Build Docker Image
```powershell
docker build -t dogansystem:latest .
```

### Run Container
```powershell
docker run -d -p 8080:80 `
  -e ConnectionStrings__Default="Server=your-sql;Database=DoganSystemDb;User Id=sa;Password=your-password;TrustServerCertificate=True" `
  --name dogansystem `
  dogansystem:latest
```

---

## 🌐 Deploy to IIS (Windows Server)

### 1. Publish
```powershell
.\build.ps1 Release
```

### 2. Copy to IIS
```powershell
Copy-Item -Path "src\DoganSystem.Web.Mvc\publish\*" -Destination "C:\inetpub\wwwroot\DoganSystem" -Recurse
```

### 3. Configure IIS
- Create Application Pool: `DoganSystemAppPool` (No Managed Code)
- Create Website pointing to: `C:\inetpub\wwwroot\DoganSystem`
- Update connection string in `web.config`

---

## ✅ Verify It's Working

1. Open browser: http://localhost:5000
2. You should see the Dashboard
3. Try creating a tenant
4. Check API: http://localhost:5000/swagger

---

## 🆘 Troubleshooting

### Build Errors?
```powershell
dotnet clean
dotnet restore
dotnet build
```

### Database Connection Issues?
- Check SQL Server is running
- Verify connection string format
- Test with SQL Server Management Studio

### Can't Run Migrations?
```powershell
dotnet tool install --global dotnet-ef
dotnet ef --version
```

---

## 📚 Full Documentation

See `BUILD_AND_DEPLOY.md` for complete deployment options:
- Azure App Service
- Linux deployment
- Docker
- IIS
- Systemd services

---

**Ready to use!** 🎉
