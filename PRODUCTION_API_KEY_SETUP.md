# Production API Key Configuration

## ✅ API Key Added

The Anthropic/Claude API key has been added to production configuration:

**API Key:** `sk-ant-api03-***REDACTED***` (stored securely in production)

## 📋 Configuration Locations

### 1. .NET Application (Production)

**File:** `src/DoganSystem.Web.Mvc/appsettings.Production.json`

Added to:
```json
{
  "Anthropic": {
    "ApiKey": "sk-ant-api03-..."
  },
  "Claude": {
    "ApiKey": "sk-ant-api03-..."
  }
}
```

**User Secrets (Development):**
```powershell
cd src/DoganSystem.Web.Mvc
dotnet user-secrets set "Anthropic:ApiKey" "sk-ant-api03-..."
dotnet user-secrets set "Claude:ApiKey" "sk-ant-api03-..."
```

### 2. Python Services (Production)

**File:** `agent-setup/.env.production`

Created with:
```env
CLAUDE_API_KEY=sk-ant-api03-...
ANTHROPIC_API_KEY=sk-ant-api03-...
```

**To use in production:**
```powershell
cd agent-setup
Copy-Item .env.production .env
# Or manually edit .env and add the keys
```

## 🔒 Security Recommendations

### For Production Deployment:

1. **Use Environment Variables** (Recommended):
   ```powershell
   # Windows
   $env:ANTHROPIC_API_KEY="sk-ant-api03-..."
   
   # Or set in Azure App Service / IIS Application Settings
   ```

2. **Use Azure Key Vault** (Best Practice):
   - Store API keys in Azure Key Vault
   - Reference from appsettings using Key Vault references

3. **Use User Secrets** (Development Only):
   - Already configured for local development
   - Never commit to source control

4. **Never Commit to Git**:
   - ✅ `.env.production` is in `.gitignore`
   - ✅ `appsettings.Production.json` should NOT contain real keys in production
   - Use environment variables or Key Vault instead

## 🚀 Usage in Code

### .NET Application:
```csharp
var apiKey = configuration["Anthropic:ApiKey"] 
    ?? configuration["Claude:ApiKey"];
```

### Python Services:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
```

## 📝 Next Steps

1. **For Production Server:**
   - Set environment variable: `ANTHROPIC_API_KEY`
   - Or use Azure Key Vault
   - Remove from `appsettings.Production.json` before deployment

2. **For Python Services:**
   - Copy `.env.production` to `.env` on production server
   - Or set environment variables directly

3. **Verify Configuration:**
   ```powershell
   # .NET
   cd src/DoganSystem.Web.Mvc
   dotnet user-secrets list
   
   # Python
   cd agent-setup
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('CLAUDE_API_KEY')[:20] + '...')"
   ```

---

**Status:** ✅ **API Key configured for production environment**

**Security Note:** For actual production deployment, use Azure Key Vault or environment variables instead of storing in appsettings.Production.json file.
