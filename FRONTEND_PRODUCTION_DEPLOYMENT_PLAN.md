# 🚀 Frontend Production Deployment - Complete Guide

## Overview
Complete step-by-step guide to deploy DoganSystem frontend landing pages to full production.

---

## 📋 Pre-Deployment Checklist

### 1. Code Preparation
- [ ] All landing page components created and tested
- [ ] Public landing page route configured (`/landing`, `/`)
- [ ] Environment variables configured
- [ ] API endpoints tested
- [ ] Build passes without errors
- [ ] TypeScript compilation successful
- [ ] No console errors in browser

### 2. Content Verification
- [ ] `landing-pages.json` has all required content
- [ ] Arabic (RTL) and English content complete
- [ ] Images and assets optimized
- [ ] All links working
- [ ] SEO metadata configured

### 3. Backend API Ready
- [ ] Backend API deployed and accessible
- [ ] CORS configured for frontend domain
- [ ] API endpoints responding correctly
- [ ] Authentication flow tested

---

## 🏗️ Step-by-Step Deployment

## Phase 1: Create Landing Page Component

### 1.1 Create Public Landing Page Route
**File:** `frontend/src/app/landing/page.tsx`

```tsx
'use client';

import React from 'react';
import { Box, Container, Typography, Button, Grid, Card, CardContent } from '@mui/material';
import landingContent from '@/content/landing-pages.json';

export default function LandingPage() {
  const content = landingContent.pages.doganconsult.ar; // or .en

  return (
    <Box>
      {/* Hero Section */}
      <Box sx={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        py: 12,
        textAlign: 'center'
      }}>
        <Container maxWidth="lg">
          <Typography variant="h1" gutterBottom>
            {content.hero.headline}
          </Typography>
          <Typography variant="h5" sx={{ mb: 4 }}>
            {content.hero.subheadline}
          </Typography>
          <Button variant="contained" size="large" color="secondary">
            {content.hero.cta.primary.text}
          </Button>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h2" textAlign="center" gutterBottom>
          {content.targetAudiences.title}
        </Typography>
        <Grid container spacing={4} sx={{ mt: 4 }}>
          {content.targetAudiences.audiences.map((audience, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    {audience.title}
                  </Typography>
                  <Typography variant="body2">
                    {audience.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* AI Agents Section */}
      <Box sx={{ bgcolor: 'grey.100', py: 8 }}>
        <Container maxWidth="lg">
          <Typography variant="h2" textAlign="center" gutterBottom>
            {content.aiAgents.title}
          </Typography>
          <Grid container spacing={4} sx={{ mt: 4 }}>
            {content.aiAgents.agents.map((agent, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="h5" gutterBottom>
                      {agent.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {agent.role}
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 2 }}>
                      {agent.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Pricing Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h2" textAlign="center" gutterBottom>
          {content.pricing.title}
        </Typography>
        <Grid container spacing={4} sx={{ mt: 4 }}>
          {content.pricing.tiers.map((tier, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card sx={{
                border: tier.popular ? '2px solid' : 'none',
                borderColor: 'primary.main'
              }}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    {tier.name}
                  </Typography>
                  <Typography variant="h3" gutterBottom>
                    {tier.price}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {tier.subtitle}
                  </Typography>
                  <Button
                    variant={tier.popular ? 'contained' : 'outlined'}
                    fullWidth
                    sx={{ mt: 2 }}
                  >
                    {tier.cta.text}
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Trust Bar */}
      <Box sx={{ bgcolor: 'primary.dark', color: 'white', py: 4 }}>
        <Container maxWidth="lg">
          <Typography variant="h6" textAlign="center">
            {content.trustBar.title}
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap', mt: 2 }}>
            {content.trustBar.badges.map((badge, index) => (
              <Typography key={index} sx={{ mx: 2 }}>
                ✓ {badge.text}
              </Typography>
            ))}
          </Box>
        </Container>
      </Box>

      {/* CTA Section */}
      <Container maxWidth="lg" sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h3" gutterBottom>
          {content.cta.primary.headline}
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
          {content.cta.primary.subheadline}
        </Typography>
        <Button variant="contained" size="large" color="primary">
          {content.cta.primary.button.text}
        </Button>
      </Container>
    </Box>
  );
}
```

### 1.2 Make Landing Page the Default Route
**File:** `frontend/src/app/page.tsx`

Update to redirect to landing page for unauthenticated users:

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

## Phase 2: Build and Test Locally

### 2.1 Install Dependencies
```bash
cd d:\DoganSystem\frontend
npm install
```

### 2.2 Test Development Build
```bash
npm run dev
```
**Verify:**
- Visit `http://localhost:3000/landing`
- Check all sections render correctly
- Test Arabic/English switching
- Verify responsive design
- Check console for errors

### 2.3 Test Production Build
```bash
npm run build
npm start
```
**Verify:**
- Build completes without errors
- No TypeScript errors
- No warnings in build output
- Production build runs correctly

### 2.4 Environment Configuration
**Create:** `frontend/.env.production`

```env
NEXT_PUBLIC_API_URL=https://api.dogansystem.com
NEXT_PUBLIC_APP_NAME=DoganSystem
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_DEFAULT_LANGUAGE=ar
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

---

## Phase 3: Choose Hosting Platform

### Option A: **Vercel** (Recommended for Next.js) ⭐

**Pros:**
- ✅ Built specifically for Next.js
- ✅ Zero configuration
- ✅ Automatic HTTPS/SSL
- ✅ Global CDN
- ✅ Automatic deployments from Git
- ✅ Free tier available
- ✅ Excellent performance

**Cons:**
- ❌ Pricing scales with traffic
- ❌ Vendor lock-in

**Deployment Steps:**

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Deploy to Production**
```bash
cd d:\DoganSystem\frontend
vercel --prod
```

4. **Configure Environment Variables in Vercel Dashboard**
   - Go to https://vercel.com/dashboard
   - Select your project
   - Settings → Environment Variables
   - Add all variables from `.env.production`

5. **Configure Custom Domain**
   - Settings → Domains
   - Add `www.dogansystem.com` and `dogansystem.com`
   - Update DNS records (provided by Vercel)

---

### Option B: **Netlify** (Alternative)

**Pros:**
- ✅ Great for static sites
- ✅ Automatic HTTPS
- ✅ Good free tier
- ✅ Easy Git integration

**Cons:**
- ❌ Less optimized for Next.js than Vercel
- ❌ Requires additional configuration

**Deployment Steps:**

1. **Install Netlify CLI**
```bash
npm install -g netlify-cli
```

2. **Build the Project**
```bash
npm run build
```

3. **Deploy**
```bash
netlify deploy --prod --dir=.next
```

4. **Configure Build Settings**
   - Build command: `npm run build`
   - Publish directory: `.next`

---

### Option C: **Azure Static Web Apps**

**Pros:**
- ✅ Microsoft ecosystem integration
- ✅ Good for enterprise
- ✅ Azure integration

**Cons:**
- ❌ More complex setup
- ❌ Higher cost

**Deployment Steps:**

1. **Install Azure CLI**
```bash
# Download from: https://aka.ms/installazurecliwindows
```

2. **Login to Azure**
```bash
az login
```

3. **Create Static Web App**
```bash
az staticwebapp create \
  --name dogansystem-frontend \
  --resource-group DoganSystemRG \
  --source d:\DoganSystem\frontend \
  --location "Central US" \
  --branch main \
  --app-location "/" \
  --output-location ".next"
```

4. **Configure CI/CD**
   - Azure creates GitHub Actions workflow automatically
   - Commits to `main` branch trigger deployments

---

### Option D: **Docker + Azure App Service**

**Pros:**
- ✅ Full control
- ✅ Custom configuration
- ✅ Can run anywhere

**Cons:**
- ❌ More maintenance
- ❌ Requires Docker knowledge

**Deployment Steps:**

1. **Create Dockerfile**
**File:** `frontend/Dockerfile`

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

2. **Build Docker Image**
```bash
cd d:\DoganSystem\frontend
docker build -t dogansystem-frontend .
```

3. **Test Locally**
```bash
docker run -p 3000:3000 dogansystem-frontend
```

4. **Push to Azure Container Registry**
```bash
az acr create --name dogansystemacr --resource-group DoganSystemRG --sku Basic
az acr login --name dogansystemacr
docker tag dogansystem-frontend dogansystemacr.azurecr.io/frontend:latest
docker push dogansystemacr.azurecr.io/frontend:latest
```

5. **Deploy to Azure App Service**
```bash
az webapp create \
  --resource-group DoganSystemRG \
  --plan DoganSystemPlan \
  --name dogansystem-frontend \
  --deployment-container-image-name dogansystemacr.azurecr.io/frontend:latest
```

---

## Phase 4: Backend API Deployment

### 4.1 Choose Backend Hosting

**Option 1: IIS on Windows Server**
```powershell
# Build
cd d:\DoganSystem\src\DoganSystem.Web.Mvc
dotnet publish -c Release -o C:\Publish\DoganSystem

# Deploy to IIS
# 1. Copy files to C:\inetpub\wwwroot\DoganSystem
# 2. Create IIS Application Pool (.NET Core)
# 3. Create IIS Website pointing to folder
# 4. Bind domain and configure SSL
```

**Option 2: Azure App Service**
```bash
# Create App Service
az webapp create \
  --resource-group DoganSystemRG \
  --plan DoganSystemPlan \
  --name dogansystem-api \
  --runtime "DOTNET|8.0"

# Deploy
cd d:\DoganSystem\src\DoganSystem.Web.Mvc
dotnet publish -c Release
cd bin/Release/net8.0/publish
zip -r deploy.zip .
az webapp deployment source config-zip \
  --resource-group DoganSystemRG \
  --name dogansystem-api \
  --src deploy.zip
```

### 4.2 Configure CORS for Frontend

**File:** `src/DoganSystem.Web.Mvc/Program.cs`

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("Production", policy =>
    {
        policy.WithOrigins(
            "https://dogansystem.com",
            "https://www.dogansystem.com",
            "https://dogansystem.vercel.app" // If using Vercel
        )
        .AllowAnyMethod()
        .AllowAnyHeader()
        .AllowCredentials();
    });
});

app.UseCors("Production");
```

---

## Phase 5: Domain and DNS Configuration

### 5.1 Purchase Domain
- Register `dogansystem.com` from domain registrar (Namecheap, GoDaddy, etc.)

### 5.2 Configure DNS Records

**For Vercel:**
```
Type    Name    Value
A       @       76.76.21.21
CNAME   www     cname.vercel-dns.com
```

**For Azure:**
```
Type    Name    Value
A       @       <Azure-IP-Address>
CNAME   www     dogansystem-frontend.azurewebsites.net
```

**Backend API:**
```
Type    Name    Value
A       api     <Backend-Server-IP>
CNAME   api     dogansystem-api.azurewebsites.net
```

### 5.3 SSL/TLS Certificate
- **Vercel/Netlify:** Automatic SSL (Let's Encrypt)
- **Azure:** Enable in App Service settings
- **Custom Server:** Install Let's Encrypt certificate

---

## Phase 6: Production Environment Variables

### Frontend Environment Variables
```env
# .env.production
NEXT_PUBLIC_API_URL=https://api.dogansystem.com
NEXT_PUBLIC_APP_NAME=DoganSystem
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_DEFAULT_LANGUAGE=ar
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_SENTRY_DSN=<your-sentry-dsn>
```

### Backend Environment Variables
```bash
# Azure App Service Configuration
ASPNETCORE_ENVIRONMENT=Production
ConnectionStrings__Default=Server=<db-server>;Database=DoganSystem;...
Anthropic__ApiKey=<from-key-vault>
JWT__Secret=<strong-secret-key>
CORS__Origins=https://dogansystem.com,https://www.dogansystem.com
```

---

## Phase 7: Post-Deployment Testing

### 7.1 Functional Testing
- [ ] Landing page loads at `https://dogansystem.com`
- [ ] All sections render correctly
- [ ] Arabic/English switching works
- [ ] Links navigate correctly
- [ ] Forms submit successfully
- [ ] API calls complete without errors

### 7.2 Performance Testing
- [ ] Page load time < 3 seconds
- [ ] Lighthouse score > 90
- [ ] No console errors
- [ ] Images optimized and load quickly

### 7.3 SEO Testing
- [ ] Meta tags present
- [ ] OpenGraph tags configured
- [ ] Sitemap.xml generated
- [ ] Robots.txt configured

### 7.4 Security Testing
- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] No sensitive data exposed
- [ ] CORS configured correctly

### 7.5 Mobile Testing
- [ ] Responsive design works
- [ ] Touch interactions work
- [ ] Mobile navigation works

---

## Phase 8: Monitoring and Analytics

### 8.1 Set Up Error Tracking
**Install Sentry:**
```bash
npm install @sentry/nextjs
```

**Configure:** `frontend/sentry.client.config.js`
```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: "production",
  tracesSampleRate: 1.0,
});
```

### 8.2 Set Up Analytics
**Google Analytics:**
```bash
npm install @next/third-parties
```

**Configure in:** `frontend/src/app/layout.tsx`
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

### 8.3 Application Monitoring
- Azure Application Insights
- Vercel Analytics
- Custom logging

---

## 📊 Production Checklist

### Pre-Launch
- [ ] All components created and tested
- [ ] Environment variables configured
- [ ] Build passes without errors
- [ ] Lighthouse score > 90
- [ ] Security scan passed
- [ ] Load testing completed

### Deployment
- [ ] Frontend deployed to hosting
- [ ] Backend API deployed and accessible
- [ ] DNS configured and propagated
- [ ] SSL certificates active
- [ ] CORS configured
- [ ] Environment variables set

### Post-Launch
- [ ] Landing page accessible at domain
- [ ] All features working
- [ ] No errors in logs
- [ ] Monitoring/analytics active
- [ ] Backup plan ready
- [ ] Documentation updated

---

## 🚀 Quick Start Commands

### Recommended: Deploy with Vercel
```bash
# 1. Build and test
cd d:\DoganSystem\frontend
npm run build
npm start

# 2. Deploy to production
vercel --prod

# 3. Configure domain in Vercel dashboard
```

### Alternative: Deploy with Docker + Azure
```bash
# 1. Build Docker image
docker build -t dogansystem-frontend .

# 2. Push to Azure Container Registry
az acr login --name dogansystemacr
docker tag dogansystem-frontend dogansystemacr.azurecr.io/frontend:latest
docker push dogansystemacr.azurecr.io/frontend:latest

# 3. Deploy to Azure
az webapp create --name dogansystem-frontend --deployment-container-image-name dogansystemacr.azurecr.io/frontend:latest
```

---

## 🎯 Production URLs

After deployment, your application will be accessible at:

- **Landing Page:** https://dogansystem.com
- **Authenticated Dashboard:** https://dogansystem.com/dashboard
- **Backend API:** https://api.dogansystem.com
- **API Documentation:** https://api.dogansystem.com/swagger

---

## 📞 Support and Maintenance

### Monitoring
- Check error logs daily
- Review analytics weekly
- Performance testing monthly

### Updates
- Security patches: Immediate
- Feature updates: Bi-weekly
- Dependency updates: Monthly

### Backup
- Database: Daily automated backups
- Code: Git repository (always backed up)
- Configuration: Document all changes

---

## ✅ Deployment Complete

Your DoganSystem landing page is now live in full production! 🎉

**Next Steps:**
1. Monitor initial traffic and errors
2. Gather user feedback
3. Optimize based on analytics
4. Plan feature enhancements

---

**Document Version:** 1.0
**Last Updated:** 2026-01-10
**Status:** ✅ Ready for Production Deployment
