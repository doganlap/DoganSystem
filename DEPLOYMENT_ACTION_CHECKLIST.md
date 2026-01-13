# 🎯 Detailed Action Checklist - Production Deployment

## Complete step-by-step actions to fulfill the deployment plan

---

# SECTION 1: CODE PREPARATION (Day 1 - Morning)

## ✅ Task 1.1: Create Landing Page Component
**Time:** 30 minutes
**Location:** `frontend/src/app/landing/page.tsx`

### Actions:
1. [ ] Open VS Code
2. [ ] Navigate to `d:\DoganSystem\frontend\src\app`
3. [ ] Create new folder: `landing`
4. [ ] Create file: `landing/page.tsx`
5. [ ] Copy the landing page code from the deployment guide
6. [ ] Save the file

**Verification:**
```bash
# Check file exists
dir d:\DoganSystem\frontend\src\app\landing\page.tsx
```

---

## ✅ Task 1.2: Update Home Page Route
**Time:** 10 minutes
**Location:** `frontend/src/app/page.tsx`

### Actions:
1. [ ] Open `frontend/src/app/page.tsx`
2. [ ] Replace content with redirect logic (from guide)
3. [ ] Save the file

**Code to add:**
```tsx
'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

export default function Home() {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading) {
      if (user) {
        router.push('/dashboard');
      } else {
        router.push('/landing');
      }
    }
  }, [user, loading, router]);

  return <div>Loading...</div>;
}
```

---

## ✅ Task 1.3: Create Production Environment File
**Time:** 5 minutes
**Location:** `frontend/.env.production`

### Actions:
1. [ ] Navigate to `d:\DoganSystem\frontend`
2. [ ] Create file: `.env.production`
3. [ ] Add environment variables:

```env
NEXT_PUBLIC_API_URL=https://api.dogansystem.com
NEXT_PUBLIC_APP_NAME=DoganSystem
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_DEFAULT_LANGUAGE=ar
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

4. [ ] Save the file

**Verification:**
```bash
cat frontend/.env.production
```

---

## ✅ Task 1.4: Install Dependencies
**Time:** 5 minutes

### Actions:
```bash
cd d:\DoganSystem\frontend
npm install
```

**Verification:**
- [ ] No errors in installation
- [ ] `node_modules` folder exists
- [ ] `package-lock.json` updated

---

# SECTION 2: LOCAL TESTING (Day 1 - Afternoon)

## ✅ Task 2.1: Test Development Build
**Time:** 15 minutes

### Actions:
```bash
cd d:\DoganSystem\frontend
npm run dev
```

### Verification Steps:
1. [ ] Open browser: `http://localhost:3000`
2. [ ] Verify redirect to `/landing`
3. [ ] Check Hero section loads
4. [ ] Check Features section loads
5. [ ] Check AI Agents section loads
6. [ ] Check Pricing section loads
7. [ ] Check Trust Bar loads
8. [ ] Check CTA section loads
9. [ ] Test Arabic/English switch (if implemented)
10. [ ] Open browser DevTools (F12)
11. [ ] Check Console tab - no errors
12. [ ] Check Network tab - all requests succeed

**Stop dev server:** Press `Ctrl+C`

---

## ✅ Task 2.2: Test Production Build
**Time:** 10 minutes

### Actions:
```bash
cd d:\DoganSystem\frontend
npm run build
```

### Verification:
1. [ ] Build completes successfully
2. [ ] No TypeScript errors
3. [ ] No build warnings
4. [ ] `.next` folder created

### Start production server:
```bash
npm start
```

### Verification:
1. [ ] Server starts on port 3000
2. [ ] Visit `http://localhost:3000/landing`
3. [ ] All sections render correctly
4. [ ] No console errors

**Stop server:** Press `Ctrl+C`

---

# SECTION 3: HOSTING SETUP (Day 1 - Evening)

## ✅ Task 3.1: Choose Hosting Platform

### Decision Matrix:
| Platform | Best For | Cost | Setup Time |
|----------|----------|------|------------|
| **Vercel** ⭐ | Next.js apps | Free tier | 10 min |
| **Netlify** | Static sites | Free tier | 15 min |
| **Azure** | Enterprise | Pay-as-go | 30 min |
| **Docker** | Full control | Variable | 60 min |

**Recommended:** Vercel

---

## ✅ Task 3.2: Deploy to Vercel (Recommended)
**Time:** 15 minutes

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

**Verification:**
```bash
vercel --version
```

### Step 2: Login to Vercel
```bash
vercel login
```

**Actions:**
1. [ ] Choose login method (GitHub/Email)
2. [ ] Complete authentication
3. [ ] Verify login successful

### Step 3: Deploy to Production
```bash
cd d:\DoganSystem\frontend
vercel --prod
```

**Follow prompts:**
1. [ ] Set up and deploy? **Yes**
2. [ ] Which scope? **Your account**
3. [ ] Link to existing project? **No**
4. [ ] Project name? **dogansystem**
5. [ ] Directory? **./  (default)**
6. [ ] Override settings? **No**

**Wait for deployment** (2-5 minutes)

### Step 4: Note Deployment URL
Vercel will provide a URL like:
```
https://dogansystem.vercel.app
```

1. [ ] Copy this URL
2. [ ] Test the URL in browser
3. [ ] Verify landing page loads

---

## ✅ Task 3.3: Configure Vercel Environment Variables
**Time:** 10 minutes

### Actions:
1. [ ] Go to https://vercel.com/dashboard
2. [ ] Click on your project: **dogansystem**
3. [ ] Go to **Settings** tab
4. [ ] Click **Environment Variables**
5. [ ] Add each variable:

**Variables to add:**
| Name | Value | Environment |
|------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://api.dogansystem.com` | Production |
| `NEXT_PUBLIC_APP_NAME` | `DoganSystem` | Production |
| `NEXT_PUBLIC_ENVIRONMENT` | `production` | Production |
| `NEXT_PUBLIC_DEFAULT_LANGUAGE` | `ar` | Production |
| `NEXT_PUBLIC_ENABLE_ANALYTICS` | `true` | Production |

6. [ ] Click **Save**
7. [ ] Redeploy to apply changes:

```bash
vercel --prod
```

---

# SECTION 4: BACKEND API DEPLOYMENT (Day 2 - Morning)

## ✅ Task 4.1: Prepare Backend for Production
**Time:** 20 minutes

### Step 1: Configure CORS for Frontend

**File:** `src/DoganSystem.Web.Mvc/Program.cs`

1. [ ] Open file in VS Code
2. [ ] Find `builder.Services.AddCors` section
3. [ ] Add production policy:

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("Production", policy =>
    {
        policy.WithOrigins(
            "https://dogansystem.com",
            "https://www.dogansystem.com",
            "https://dogansystem.vercel.app"
        )
        .AllowAnyMethod()
        .AllowAnyHeader()
        .AllowCredentials();
    });
});

// Add before app.UseAuthorization()
app.UseCors("Production");
```

4. [ ] Save file

### Step 2: Build Backend for Production
```bash
cd d:\DoganSystem\src\DoganSystem.Web.Mvc
dotnet publish -c Release -o d:\Publish\DoganSystem
```

**Verification:**
1. [ ] Build completes successfully
2. [ ] No compilation errors
3. [ ] Files created in `d:\Publish\DoganSystem`

---

## ✅ Task 4.2: Deploy Backend to IIS (Option A)
**Time:** 30 minutes

### Prerequisites:
1. [ ] Windows Server with IIS installed
2. [ ] .NET 8 Hosting Bundle installed
3. [ ] SQL Server accessible

### Step 1: Copy Files to Server
```bash
# Copy published files to server
xcopy d:\Publish\DoganSystem C:\inetpub\wwwroot\DoganSystem /E /I /Y
```

### Step 2: Create IIS Application Pool
1. [ ] Open IIS Manager
2. [ ] Right-click **Application Pools**
3. [ ] Click **Add Application Pool**
4. [ ] Name: `DoganSystemPool`
5. [ ] .NET CLR Version: **No Managed Code**
6. [ ] Managed Pipeline Mode: **Integrated**
7. [ ] Click **OK**

### Step 3: Configure Application Pool
1. [ ] Select `DoganSystemPool`
2. [ ] Click **Advanced Settings**
3. [ ] Set **Identity** to `ApplicationPoolIdentity`
4. [ ] Set **Start Mode** to `AlwaysRunning`
5. [ ] Click **OK**

### Step 4: Create IIS Website
1. [ ] Right-click **Sites**
2. [ ] Click **Add Website**
3. [ ] Site name: `DoganSystem`
4. [ ] Application Pool: `DoganSystemPool`
5. [ ] Physical path: `C:\inetpub\wwwroot\DoganSystem`
6. [ ] Binding:
   - Type: `http`
   - IP: `All Unassigned`
   - Port: `80`
   - Host name: `api.dogansystem.com`
7. [ ] Click **OK**

### Step 5: Configure SSL
1. [ ] Select site: `DoganSystem`
2. [ ] Click **Bindings**
3. [ ] Click **Add**
4. [ ] Type: `https`
5. [ ] Port: `443`
6. [ ] SSL Certificate: **Select your certificate**
7. [ ] Click **OK**

### Step 6: Set Environment Variables
```powershell
# Run PowerShell as Administrator
cd C:\inetpub\wwwroot\DoganSystem

# Create web.config environment variables
@"
<configuration>
  <location path="." inheritInChildApplications="false">
    <system.webServer>
      <aspNetCore processPath="dotnet"
                  arguments=".\DoganSystem.Web.Mvc.dll"
                  stdoutLogEnabled="false"
                  stdoutLogFile=".\logs\stdout"
                  hostingModel="inprocess">
        <environmentVariables>
          <environmentVariable name="ASPNETCORE_ENVIRONMENT" value="Production" />
        </environmentVariables>
      </aspNetCore>
    </system.webServer>
  </location>
</configuration>
"@ | Out-File web.config -Encoding UTF8
```

### Step 7: Configure appsettings.Production.json
```bash
# Edit appsettings.Production.json
notepad C:\inetpub\wwwroot\DoganSystem\appsettings.Production.json
```

**Add/Update:**
```json
{
  "ConnectionStrings": {
    "Default": "Server=YOUR_SQL_SERVER;Database=DoganSystem;User Id=sa;Password=YOUR_PASSWORD;TrustServerCertificate=True;"
  },
  "Anthropic": {
    "ApiKey": "YOUR_API_KEY_FROM_AZURE_KEY_VAULT"
  },
  "Cors": {
    "Origins": "https://dogansystem.com,https://www.dogansystem.com,https://dogansystem.vercel.app"
  },
  "App": {
    "ServerRootAddress": "https://api.dogansystem.com"
  }
}
```

### Step 8: Restart Website
1. [ ] Select site in IIS Manager
2. [ ] Click **Restart** in Actions panel
3. [ ] Verify site is running

**Test:**
```bash
curl https://api.dogansystem.com/api/health
```

---

## ✅ Task 4.3: Deploy Backend to Azure (Option B)
**Time:** 25 minutes

### Step 1: Install Azure CLI
```bash
# Download and install from:
# https://aka.ms/installazurecliwindows
```

### Step 2: Login to Azure
```bash
az login
```

### Step 3: Create Resource Group
```bash
az group create --name DoganSystemRG --location "Central US"
```

### Step 4: Create App Service Plan
```bash
az appservice plan create `
  --name DoganSystemPlan `
  --resource-group DoganSystemRG `
  --sku B1 `
  --is-linux
```

### Step 5: Create Web App
```bash
az webapp create `
  --resource-group DoganSystemRG `
  --plan DoganSystemPlan `
  --name dogansystem-api `
  --runtime "DOTNET:8.0"
```

### Step 6: Configure Environment Variables
```bash
az webapp config appsettings set `
  --resource-group DoganSystemRG `
  --name dogansystem-api `
  --settings ASPNETCORE_ENVIRONMENT=Production
```

### Step 7: Deploy Application
```bash
cd d:\DoganSystem\src\DoganSystem.Web.Mvc
dotnet publish -c Release

# Create deployment package
cd bin\Release\net8.0\publish
Compress-Archive -Path * -DestinationPath deploy.zip -Force

# Deploy to Azure
az webapp deployment source config-zip `
  --resource-group DoganSystemRG `
  --name dogansystem-api `
  --src deploy.zip
```

### Step 8: Configure Custom Domain
```bash
az webapp config hostname add `
  --webapp-name dogansystem-api `
  --resource-group DoganSystemRG `
  --hostname api.dogansystem.com
```

### Step 9: Enable HTTPS
```bash
az webapp update `
  --resource-group DoganSystemRG `
  --name dogansystem-api `
  --https-only true
```

**Test:**
```bash
curl https://dogansystem-api.azurewebsites.net/api/health
```

---

# SECTION 5: DOMAIN & DNS CONFIGURATION (Day 2 - Afternoon)

## ✅ Task 5.1: Purchase Domain
**Time:** 15 minutes

### Actions:
1. [ ] Go to domain registrar (Namecheap, GoDaddy, etc.)
2. [ ] Search for: `dogansystem.com`
3. [ ] Purchase domain (if available)
4. [ ] Complete registration

**Alternative:** Use existing domain

---

## ✅ Task 5.2: Configure DNS Records
**Time:** 10 minutes

### For Vercel Frontend:

1. [ ] Login to domain registrar
2. [ ] Go to DNS Management
3. [ ] Add DNS records:

**Record 1: Root domain**
```
Type: A
Name: @
Value: 76.76.21.21
TTL: Automatic
```

**Record 2: WWW subdomain**
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: Automatic
```

### For Backend API:

**If using IIS:**
```
Type: A
Name: api
Value: YOUR_SERVER_IP_ADDRESS
TTL: Automatic
```

**If using Azure:**
```
Type: CNAME
Name: api
Value: dogansystem-api.azurewebsites.net
TTL: Automatic
```

4. [ ] Save DNS changes
5. [ ] Wait for DNS propagation (5-60 minutes)

**Check DNS propagation:**
```bash
nslookup dogansystem.com
nslookup www.dogansystem.com
nslookup api.dogansystem.com
```

---

## ✅ Task 5.3: Configure Custom Domain in Vercel
**Time:** 5 minutes

### Actions:
1. [ ] Go to https://vercel.com/dashboard
2. [ ] Select project: **dogansystem**
3. [ ] Go to **Settings** → **Domains**
4. [ ] Click **Add Domain**
5. [ ] Enter: `dogansystem.com`
6. [ ] Click **Add**
7. [ ] Add second domain: `www.dogansystem.com`
8. [ ] Verify DNS configuration

Vercel will automatically provision SSL certificates.

**Test:**
```bash
curl https://dogansystem.com
curl https://www.dogansystem.com
```

---

# SECTION 6: DATABASE SETUP (Day 2 - Evening)

## ✅ Task 6.1: Create Production Database
**Time:** 20 minutes

### Option A: SQL Server on Windows

```sql
-- Connect to SQL Server
-- Run in SQL Server Management Studio (SSMS)

-- Create database
CREATE DATABASE DoganSystem;
GO

-- Create user
CREATE LOGIN DoganSystemUser WITH PASSWORD = 'StrongPassword123!';
GO

USE DoganSystem;
CREATE USER DoganSystemUser FOR LOGIN DoganSystemUser;
ALTER ROLE db_owner ADD MEMBER DoganSystemUser;
GO
```

### Option B: Azure SQL Database

```bash
# Create Azure SQL Server
az sql server create `
  --name dogansystem-sql `
  --resource-group DoganSystemRG `
  --location "Central US" `
  --admin-user sqladmin `
  --admin-password "StrongPassword123!"

# Create database
az sql db create `
  --resource-group DoganSystemRG `
  --server dogansystem-sql `
  --name DoganSystem `
  --service-objective S0

# Configure firewall (allow Azure services)
az sql server firewall-rule create `
  --resource-group DoganSystemRG `
  --server dogansystem-sql `
  --name AllowAzureServices `
  --start-ip-address 0.0.0.0 `
  --end-ip-address 0.0.0.0
```

---

## ✅ Task 6.2: Run Database Migrations
**Time:** 10 minutes

### Actions:
```bash
cd d:\DoganSystem\src\DoganSystem.Web.Mvc

# Update connection string in appsettings.json temporarily
# Or use environment variable

$env:ConnectionStrings__Default="Server=YOUR_SERVER;Database=DoganSystem;User Id=sqladmin;Password=StrongPassword123!;TrustServerCertificate=True;"

# Run migrations
dotnet ef database update

# Verify tables created
# Connect to database and check tables exist
```

**Verification:**
- [ ] Database created
- [ ] All tables exist
- [ ] No migration errors

---

## ✅ Task 6.3: Seed Initial Data
**Time:** 5 minutes

### Actions:
```bash
# Run the application once to seed data
cd d:\DoganSystem\src\DoganSystem.Web.Mvc
dotnet run --environment Production
```

**Or use SQL script:**
```sql
-- Insert default admin user
INSERT INTO AbpUsers (UserName, EmailAddress, Name, Surname, IsEmailConfirmed, Password)
VALUES ('admin', 'admin@dogansystem.com', 'System', 'Administrator', 1, 'HASHED_PASSWORD');
```

---

# SECTION 7: TESTING & VERIFICATION (Day 3 - Morning)

## ✅ Task 7.1: Functional Testing
**Time:** 30 minutes

### Frontend Tests:
1. [ ] Visit `https://dogansystem.com`
2. [ ] Verify landing page loads
3. [ ] Check Hero section displays correctly
4. [ ] Check Features section displays correctly
5. [ ] Check AI Agents section displays correctly
6. [ ] Check Pricing section displays correctly
7. [ ] Check Trust Bar displays correctly
8. [ ] Check CTA section displays correctly
9. [ ] Test "Get Started" button
10. [ ] Test navigation links
11. [ ] Test language switcher (if implemented)
12. [ ] Test on mobile device
13. [ ] Test on tablet
14. [ ] Test on desktop

### Backend API Tests:
```bash
# Test health endpoint
curl https://api.dogansystem.com/api/health

# Test authentication
curl -X POST https://api.dogansystem.com/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{"username":"admin","password":"admin123"}'

# Test tenant endpoint
curl https://api.dogansystem.com/api/tenants `
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Checklist:**
- [ ] Health endpoint responds
- [ ] Authentication works
- [ ] API endpoints return data
- [ ] CORS headers present
- [ ] No 500 errors

---

## ✅ Task 7.2: Performance Testing
**Time:** 20 minutes

### Use Lighthouse (Chrome DevTools):
1. [ ] Open Chrome
2. [ ] Navigate to `https://dogansystem.com`
3. [ ] Open DevTools (F12)
4. [ ] Go to **Lighthouse** tab
5. [ ] Select **Performance, SEO, Best Practices, Accessibility**
6. [ ] Click **Analyze page load**
7. [ ] Wait for report

**Target Scores:**
- [ ] Performance: > 90
- [ ] Accessibility: > 90
- [ ] Best Practices: > 90
- [ ] SEO: > 90

### Check Page Load Time:
1. [ ] Open DevTools → Network tab
2. [ ] Reload page (Ctrl+Shift+R)
3. [ ] Check **Load** time at bottom

**Target:**
- [ ] Page load < 3 seconds
- [ ] First Contentful Paint < 1.5s
- [ ] Largest Contentful Paint < 2.5s

---

## ✅ Task 7.3: Security Testing
**Time:** 15 minutes

### SSL/HTTPS Check:
1. [ ] Visit `https://www.ssllabs.com/ssltest`
2. [ ] Enter: `dogansystem.com`
3. [ ] Click **Submit**
4. [ ] Wait for results

**Target:**
- [ ] Grade A or A+
- [ ] TLS 1.2+ supported
- [ ] Valid certificate

### Security Headers Check:
```bash
curl -I https://dogansystem.com
```

**Verify headers:**
- [ ] `Strict-Transport-Security` present
- [ ] `X-Content-Type-Options: nosniff` present
- [ ] `X-Frame-Options: DENY` present
- [ ] `Content-Security-Policy` present

### CORS Check:
```bash
curl -H "Origin: https://dogansystem.com" `
  -H "Access-Control-Request-Method: POST" `
  -H "Access-Control-Request-Headers: Content-Type" `
  -X OPTIONS `
  https://api.dogansystem.com/api/tenants -v
```

**Verify:**
- [ ] `Access-Control-Allow-Origin` header present
- [ ] `Access-Control-Allow-Methods` includes required methods
- [ ] `Access-Control-Allow-Credentials: true`

---

## ✅ Task 7.4: Mobile Responsiveness Testing
**Time:** 10 minutes

### Test on Different Devices:
1. [ ] iPhone 12 Pro (390x844)
2. [ ] Samsung Galaxy S21 (360x800)
3. [ ] iPad (768x1024)
4. [ ] Desktop (1920x1080)

### Use Chrome DevTools:
1. [ ] Open DevTools (F12)
2. [ ] Click **Toggle Device Toolbar** (Ctrl+Shift+M)
3. [ ] Select device
4. [ ] Verify layout

**Checklist:**
- [ ] Text is readable
- [ ] Images scale correctly
- [ ] Buttons are tappable (min 44x44px)
- [ ] No horizontal scrolling
- [ ] Navigation works on mobile

---

# SECTION 8: MONITORING & ANALYTICS (Day 3 - Afternoon)

## ✅ Task 8.1: Set Up Error Tracking (Sentry)
**Time:** 15 minutes

### Step 1: Create Sentry Account
1. [ ] Go to https://sentry.io
2. [ ] Sign up for free account
3. [ ] Create new project: **DoganSystem**
4. [ ] Select platform: **Next.js**
5. [ ] Copy DSN

### Step 2: Install Sentry in Frontend
```bash
cd d:\DoganSystem\frontend
npx @sentry/wizard@latest -i nextjs
```

### Step 3: Configure Sentry
**File:** `frontend/sentry.client.config.js`

```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  environment: "production",
  tracesSampleRate: 1.0,
  beforeSend(event, hint) {
    // Filter sensitive data
    return event;
  },
});
```

### Step 4: Test Error Tracking
```javascript
// Add to a page to test
throw new Error("Test Sentry error");
```

### Step 5: Deploy with Sentry
```bash
vercel --prod
```

**Verification:**
1. [ ] Trigger test error
2. [ ] Check Sentry dashboard for error
3. [ ] Verify error captured correctly

---

## ✅ Task 8.2: Set Up Google Analytics
**Time:** 10 minutes

### Step 1: Create GA4 Property
1. [ ] Go to https://analytics.google.com
2. [ ] Create account: **DoganSystem**
3. [ ] Create property: **DoganSystem Website**
4. [ ] Select **Web** platform
5. [ ] Copy Measurement ID (G-XXXXXXXXXX)

### Step 2: Install Analytics in Frontend
```bash
cd d:\DoganSystem\frontend
npm install @next/third-parties
```

### Step 3: Configure in Layout
**File:** `frontend/src/app/layout.tsx`

```tsx
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>{children}</body>
      <GoogleAnalytics gaId="G-XXXXXXXXXX" />
    </html>
  )
}
```

### Step 4: Add to Vercel Environment
1. [ ] Vercel Dashboard → Environment Variables
2. [ ] Add: `NEXT_PUBLIC_GA_MEASUREMENT_ID` = `G-XXXXXXXXXX`
3. [ ] Redeploy

**Verification:**
1. [ ] Visit website
2. [ ] Check GA Real-Time report
3. [ ] Verify page views tracked

---

## ✅ Task 8.3: Set Up Application Insights (Azure)
**Time:** 15 minutes

### Step 1: Create Application Insights
```bash
az monitor app-insights component create `
  --app dogansystem-insights `
  --location "Central US" `
  --resource-group DoganSystemRG
```

### Step 2: Get Instrumentation Key
```bash
az monitor app-insights component show `
  --app dogansystem-insights `
  --resource-group DoganSystemRG `
  --query instrumentationKey -o tsv
```

### Step 3: Configure in Backend
**File:** `appsettings.Production.json`

```json
{
  "ApplicationInsights": {
    "InstrumentationKey": "YOUR_INSTRUMENTATION_KEY"
  }
}
```

### Step 4: Install NuGet Package
```bash
cd d:\DoganSystem\src\DoganSystem.Web.Mvc
dotnet add package Microsoft.ApplicationInsights.AspNetCore
```

### Step 5: Configure in Program.cs
```csharp
builder.Services.AddApplicationInsightsTelemetry();
```

### Step 6: Deploy Backend
```bash
# Rebuild and redeploy
dotnet publish -c Release
```

**Verification:**
1. [ ] Make API requests
2. [ ] Check Application Insights in Azure Portal
3. [ ] Verify telemetry data appears

---

# SECTION 9: PRODUCTION ENVIRONMENT VARIABLES (Day 3)

## ✅ Task 9.1: Configure All Environment Variables

### Frontend (Vercel):
1. [ ] Go to Vercel Dashboard
2. [ ] Project Settings → Environment Variables
3. [ ] Add all variables:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://api.dogansystem.com` |
| `NEXT_PUBLIC_APP_NAME` | `DoganSystem` |
| `NEXT_PUBLIC_ENVIRONMENT` | `production` |
| `NEXT_PUBLIC_GA_MEASUREMENT_ID` | `G-XXXXXXXXXX` |
| `NEXT_PUBLIC_SENTRY_DSN` | `https://xxx@sentry.io/xxx` |

### Backend (Azure App Service):
```bash
az webapp config appsettings set `
  --name dogansystem-api `
  --resource-group DoganSystemRG `
  --settings `
    ASPNETCORE_ENVIRONMENT=Production `
    APPLICATIONINSIGHTS_CONNECTION_STRING="YOUR_CONNECTION_STRING" `
    ANTHROPIC_API_KEY="YOUR_API_KEY"
```

### Backend (IIS):
```powershell
# Set machine-level environment variables
[System.Environment]::SetEnvironmentVariable("ASPNETCORE_ENVIRONMENT", "Production", "Machine")
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "YOUR_API_KEY", "Machine")

# Restart IIS
iisreset
```

---

# SECTION 10: FINAL VERIFICATION (Day 3 - Evening)

## ✅ Task 10.1: Complete Production Checklist

### Pre-Launch Checklist:
- [ ] Landing page loads correctly
- [ ] All sections render properly
- [ ] API endpoints working
- [ ] Database connected
- [ ] Authentication working
- [ ] CORS configured
- [ ] SSL certificates active
- [ ] DNS propagated
- [ ] Environment variables set
- [ ] Monitoring active
- [ ] Error tracking working
- [ ] Analytics tracking
- [ ] Mobile responsive
- [ ] Performance score > 90
- [ ] Security scan passed
- [ ] No console errors
- [ ] No broken links

### Post-Launch Checklist:
- [ ] Monitor error logs for 24 hours
- [ ] Check analytics for traffic
- [ ] Verify all features working
- [ ] Test contact forms
- [ ] Test user registration
- [ ] Monitor server resources
- [ ] Check database performance
- [ ] Verify backups running

---

## ✅ Task 10.2: Document Deployment

### Create Deployment Report:
```markdown
# Deployment Report - DoganSystem

**Date:** 2026-01-XX
**Deployed By:** [Your Name]

## Deployed Components:
- [x] Frontend: https://dogansystem.com
- [x] Backend API: https://api.dogansystem.com
- [x] Database: SQL Server / Azure SQL

## Deployment Details:
- **Frontend Host:** Vercel
- **Backend Host:** Azure / IIS
- **Database:** Azure SQL / SQL Server
- **Domain:** dogansystem.com
- **SSL:** Active (Grade A)

## Performance Metrics:
- **Lighthouse Score:** XX/100
- **Page Load Time:** X.Xs
- **API Response Time:** XXXms

## Monitoring:
- **Error Tracking:** Sentry
- **Analytics:** Google Analytics
- **Application Insights:** Azure

## Known Issues:
- None

## Next Steps:
1. Monitor for 48 hours
2. Gather user feedback
3. Plan feature enhancements
```

---

# QUICK REFERENCE COMMANDS

## Frontend Deployment:
```bash
cd d:\DoganSystem\frontend
npm run build
vercel --prod
```

## Backend Deployment (IIS):
```bash
cd d:\DoganSystem\src\DoganSystem.Web.Mvc
dotnet publish -c Release -o C:\Publish\DoganSystem
xcopy C:\Publish\DoganSystem C:\inetpub\wwwroot\DoganSystem /E /I /Y
iisreset
```

## Backend Deployment (Azure):
```bash
cd d:\DoganSystem\src\DoganSystem.Web.Mvc
dotnet publish -c Release
cd bin\Release\net8.0\publish
Compress-Archive -Path * -DestinationPath deploy.zip -Force
az webapp deployment source config-zip --resource-group DoganSystemRG --name dogansystem-api --src deploy.zip
```

## Check Deployment Status:
```bash
curl https://dogansystem.com
curl https://api.dogansystem.com/api/health
```

---

# TROUBLESHOOTING

## Issue: Landing page shows 404
**Solution:**
1. Check Vercel deployment logs
2. Verify `landing/page.tsx` exists
3. Redeploy: `vercel --prod`

## Issue: API CORS errors
**Solution:**
1. Check CORS configuration in Program.cs
2. Verify frontend domain in CORS policy
3. Restart backend application

## Issue: Database connection failed
**Solution:**
1. Check connection string
2. Verify SQL Server accessible
3. Check firewall rules
4. Test connection manually

## Issue: SSL certificate error
**Solution:**
1. Verify DNS records
2. Check domain verification in hosting
3. Wait for certificate provisioning (can take 1 hour)

## Issue: Environment variables not working
**Solution:**
1. Verify variables set correctly
2. Check variable names (case-sensitive)
3. Redeploy application
4. Restart server/app service

---

**Document Version:** 1.0
**Last Updated:** 2026-01-10
**Status:** ✅ Ready for Execution

**Estimated Total Time:** 2-3 days
**Difficulty:** Medium
**Prerequisites:** Basic knowledge of web deployment, Azure/IIS, DNS configuration
