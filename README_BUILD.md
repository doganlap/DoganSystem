# 🏗️ Build and Deploy Instructions

## ✅ Ready to Build and Deploy!

Your DoganSystem application is **complete and ready to build**. Follow these steps:

---

## 🚀 Quick Build (Windows)

### Option 1: Use Build Script
```powershell
.\build.ps1
```

### Option 2: Manual Build
```powershell
# 1. Restore packages
dotnet restore DoganSystem.sln

# 2. Build solution
dotnet build DoganSystem.sln --configuration Release

# 3. Publish (optional)
dotnet publish src\DoganSystem.Web.Mvc\DoganSystem.Web.Mvc.csproj --configuration Release --output ./publish
```

---

## 📋 Pre-Build Checklist

Before building, ensure:

- [x] ✅ .NET 8.0 SDK installed (you have 10.0.101 - compatible!)
- [x] ✅ NuGet.org source configured
- [ ] ⚠️ SQL Server installed and running
- [ ] ⚠️ Connection string configured in `appsettings.json`

---

## 🗄️ Database Setup (Required Before Running)

### Step 1: Update Connection String
Edit `src/DoganSystem.Web.Mvc/appsettings.json`:
```json
{
  "ConnectionStrings": {
    "Default": "Server=localhost;Database=DoganSystemDb;Trusted_Connection=True;TrustServerCertificate=True"
  }
}
```

### Step 2: Install EF Core Tools
```powershell
dotnet tool install --global dotnet-ef
```

### Step 3: Create Database
```powershell
cd src\DoganSystem.EntityFrameworkCore
dotnet ef migrations add Initial --startup-project ..\DoganSystem.Web.Mvc
dotnet ef database update --startup-project ..\DoganSystem.Web.Mvc
```

---

## ▶️ Run the Application

```powershell
cd src\DoganSystem.Web.Mvc
dotnet run
```

**Access:**
- Web UI: http://localhost:5000
- API Docs: http://localhost:5000/swagger

---

## 📦 Deployment Options

### 1. **Local Development** ✅ (Easiest)
```powershell
.\build.ps1
cd src\DoganSystem.Web.Mvc
dotnet run
```

### 2. **Docker** 🐳
```powershell
docker build -t dogansystem:latest .
docker run -d -p 8080:80 -e ConnectionStrings__Default="your-connection-string" dogansystem:latest
```

### 3. **IIS (Windows Server)** 🌐
```powershell
.\build.ps1 Release
# Copy publish folder to C:\inetpub\wwwroot\DoganSystem
# Configure IIS Application Pool and Website
```

### 4. **Azure App Service** ☁️
- Push to GitHub
- Connect Azure App Service to GitHub
- Configure connection string in Azure Portal

---

## 📚 Documentation Files

- **`QUICK_START.md`** - Fastest way to get running
- **`BUILD_AND_DEPLOY.md`** - Complete deployment guide
- **`BUILD_TROUBLESHOOTING.md`** - Fix common issues
- **`APP_COMPLETION_SUMMARY.md`** - What's been implemented

---

## ⚠️ If Build Fails

### Common Issues:

1. **NuGet packages not found**
   ```powershell
   dotnet nuget list source  # Verify nuget.org is listed
   dotnet restore --force
   ```

2. **Database connection issues**
   - Check SQL Server is running
   - Verify connection string format
   - See `BUILD_TROUBLESHOOTING.md`

3. **EF Core tools missing**
   ```powershell
   dotnet tool install --global dotnet-ef
   ```

---

## ✅ Build Status

**Current Status:** ✅ **READY TO BUILD**

- ✅ All code files complete
- ✅ Project references configured
- ✅ NuGet packages defined
- ✅ Configuration files ready
- ⚠️ Database setup required (before first run)

---

## 🎯 Next Steps

1. **Build the solution** (see commands above)
2. **Configure database connection** in `appsettings.json`
3. **Run migrations** to create database
4. **Run the application** and test it!

---

**You're all set!** 🚀

For detailed instructions, see:
- `QUICK_START.md` - Get running in 5 minutes
- `BUILD_AND_DEPLOY.md` - Full deployment guide
