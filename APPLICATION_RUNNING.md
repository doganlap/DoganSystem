# 🚀 Application Running Status

## Where is the Application Running?

### Local Development URLs

The DoganSystem application is running on your local machine at:

- **HTTP (Port 5000)**: `http://localhost:5000`
- **HTTPS (Port 5001)**: `https://localhost:5001`
- **Swagger API Docs**: `https://localhost:5001/swagger`

### Access the Application

1. **Open in Browser**:
   - Navigate to: `https://localhost:5001`
   - Or: `http://localhost:5000`

2. **View API Documentation**:
   - Navigate to: `https://localhost:5001/swagger`
   - This shows all available API endpoints

3. **Test API Endpoints**:
   ```bash
   # List tenants
   curl https://localhost:5001/api/tenants
   
   # List agents
   curl https://localhost:5001/api/agents
   
   # List subscriptions
   curl https://localhost:5001/api/subscriptions
   ```

## Application Process

The application is running as a background process. To check:

```powershell
# Check if running
Get-Process | Where-Object {$_.ProcessName -like "*dotnet*"}

# Check ports
netstat -ano | findstr ":5000 :5001"
```

## Application Location

**Source Code**: `d:\DoganSystem\src\DoganSystem.Web.Mvc`

**Published Files** (if published): `d:\DoganSystem\src\DoganSystem.Web.Mvc\publish`

**Database**: SQL Server LocalDB
- **Server**: `(localdb)\mssqllocaldb`
- **Database**: `DoganSystemDb`
- **Connection**: Configured in `appsettings.json`

## Quick Access Links

### Web Interface
- **Home Page**: [https://localhost:5001](https://localhost:5001)
- **HTTP Version**: [http://localhost:5000](http://localhost:5000)

### API Documentation
- **Swagger UI**: [https://localhost:5001/swagger](https://localhost:5001/swagger)

### API Endpoints
- **Tenants**: `https://localhost:5001/api/tenants`
- **Agents**: `https://localhost:5001/api/agents`
- **ERPNext**: `https://localhost:5001/api/erpnext`
- **Subscriptions**: `https://localhost:5001/api/subscriptions`

## Stop the Application

To stop the running application:

1. **Find the Process**:
   ```powershell
   Get-Process | Where-Object {$_.ProcessName -like "*dotnet*"}
   ```

2. **Stop the Process**:
   ```powershell
   Stop-Process -Name "dotnet" -Force
   ```

Or press `Ctrl+C` in the console where it's running.

## Restart the Application

```powershell
cd d:\DoganSystem\src\DoganSystem.Web.Mvc
dotnet run --configuration Release
```

Or use the script:
```powershell
.\run-app.ps1
```

## Verify Application is Running

### Method 1: Check Browser
Open `https://localhost:5001` - you should see the application home page.

### Method 2: Check Swagger
Open `https://localhost:5001/swagger` - you should see API documentation.

### Method 3: Check API
```bash
curl https://localhost:5001/api/tenants
```
Should return JSON response (may be empty array if no tenants).

### Method 4: Check Process
```powershell
Get-Process | Where-Object {$_.ProcessName -eq "dotnet"}
```

## Application Status

✅ **Application**: Running  
✅ **Database**: Connected  
✅ **Migration**: Applied  
✅ **Roles**: Auto-seeded on startup  
✅ **API**: Available  

## Troubleshooting

### If Application Not Accessible

1. **Check if Running**:
   ```powershell
   Get-Process | Where-Object {$_.ProcessName -eq "dotnet"}
   ```

2. **Check Ports**:
   ```powershell
   netstat -ano | findstr ":5000 :5001"
   ```

3. **Check Logs**: Look at the console output for errors

4. **Restart Application**:
   ```powershell
   cd d:\DoganSystem\src\DoganSystem.Web.Mvc
   dotnet run
   ```

### If Port Already in Use

Change ports in `launchSettings.json`:
```json
{
  "applicationUrl": "https://localhost:5002;http://localhost:5003"
}
```

---

**Current Status**: ✅ Application is running at `https://localhost:5001`

**Quick Access**: Open your browser and go to `https://localhost:5001`
