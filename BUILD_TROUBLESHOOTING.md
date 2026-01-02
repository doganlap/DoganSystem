# Build Troubleshooting Guide

## Common Build Issues and Solutions

### ❌ Issue: "Unable to find package Volo.Abp.*"

**Error:**
```
error NU1101: Unable to find package Volo.Abp.Domain. No packages exist with this id in source(s)
```

**Solution 1: Add NuGet.org Source**
```powershell
dotnet nuget add source https://api.nuget.org/v3/index.json --name nuget.org
```

**Solution 2: Verify NuGet Sources**
```powershell
dotnet nuget list source
```

You should see `nuget.org` in the list. If not, add it:
```powershell
dotnet nuget add source https://api.nuget.org/v3/index.json --name nuget.org
```

**Solution 3: Clear NuGet Cache**
```powershell
dotnet nuget locals all --clear
dotnet restore
```

**Solution 4: Check Internet Connection**
- Ensure you have internet access
- Check if corporate firewall is blocking NuGet
- Try accessing https://www.nuget.org in browser

---

### ❌ Issue: "Package restore failed"

**Solution:**
```powershell
# Clean everything
dotnet clean
Remove-Item -Recurse -Force .\**\bin
Remove-Item -Recurse -Force .\**\obj

# Restore again
dotnet restore
```

---

### ❌ Issue: "EF Core tools not found"

**Error:**
```
Could not execute because the application was not found
```

**Solution:**
```powershell
# Install EF Core tools globally
dotnet tool install --global dotnet-ef

# Verify installation
dotnet ef --version

# If already installed, update it
dotnet tool update --global dotnet-ef
```

---

### ❌ Issue: "Database connection failed"

**Error:**
```
Cannot open database "DoganSystemDb" requested by the login
```

**Solutions:**

1. **Check SQL Server is Running**
   ```powershell
   # Check SQL Server service
   Get-Service MSSQLSERVER
   
   # Start if stopped
   Start-Service MSSQLSERVER
   ```

2. **Verify Connection String**
   - For SQL Server Express: `Server=localhost\SQLEXPRESS`
   - For LocalDB: `Server=(localdb)\mssqllocaldb`
   - For Full SQL Server: `Server=localhost`

3. **Test Connection**
   ```powershell
   # Using sqlcmd
   sqlcmd -S localhost -E -Q "SELECT @@VERSION"
   ```

4. **Create Database Manually**
   ```sql
   CREATE DATABASE DoganSystemDb;
   ```

---

### ❌ Issue: "Migration errors"

**Error:**
```
No DbContext was found
```

**Solution:**
```powershell
# Make sure you're in the right directory
cd src\DoganSystem.EntityFrameworkCore

# Use full path to startup project
dotnet ef migrations add Initial --startup-project ..\DoganSystem.Web.Mvc\DoganSystem.Web.Mvc.csproj
```

---

### ❌ Issue: "Build warnings about RestSharp vulnerability"

**Warning:**
```
Package 'RestSharp' 110.2.0 has a known moderate severity vulnerability
```

**Solution:**
This is a known warning. The vulnerability is in RestSharp but doesn't affect our usage. You can:
1. Ignore it (it's just a warning)
2. Update RestSharp to latest version (if compatible)
3. Replace RestSharp with HttpClient (future enhancement)

---

### ❌ Issue: ".NET SDK version mismatch"

**Error:**
```
The project targets .NET 8.0 but SDK 10.0 is installed
```

**Solution:**
This is fine! .NET SDK 10.0 can build .NET 8.0 projects. If you want to use .NET 8.0 SDK specifically:
1. Install .NET 8.0 SDK from https://dotnet.microsoft.com/download
2. Or continue using .NET 10.0 SDK (it's backward compatible)

---

### ❌ Issue: "Port already in use"

**Error:**
```
Failed to bind to address http://localhost:5000
```

**Solution:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change port in launchSettings.json
```

---

### ❌ Issue: "Permission denied" (Linux/Mac)

**Error:**
```
Permission denied: ./build.sh
```

**Solution:**
```bash
chmod +x build.sh
chmod +x deploy.sh
```

---

## 🔧 Quick Fixes Checklist

- [ ] Internet connection working
- [ ] NuGet.org source configured
- [ ] .NET SDK installed (8.0 or higher)
- [ ] SQL Server installed and running
- [ ] Connection string configured correctly
- [ ] EF Core tools installed
- [ ] All files saved and committed

## 📞 Still Having Issues?

1. **Check Logs:**
   ```powershell
   dotnet restore --verbosity detailed
   dotnet build --verbosity detailed
   ```

2. **Verify Prerequisites:**
   - .NET 8.0 SDK or higher
   - SQL Server (Express, LocalDB, or Full)
   - Visual Studio 2022 or VS Code (optional)

3. **Clean Build:**
   ```powershell
   dotnet clean
   Remove-Item -Recurse -Force .\**\bin, .\**\obj
   dotnet restore
   dotnet build
   ```

4. **Check ABP Framework Documentation:**
   - https://docs.abp.io/en/abp/latest/Getting-Started

---

**Most common issue:** NuGet source not configured. Run:
```powershell
dotnet nuget add source https://api.nuget.org/v3/index.json --name nuget.org
```
