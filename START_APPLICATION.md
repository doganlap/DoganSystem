# 🚀 How to Start the Application and Access UI

## Quick Start

### Step 1: Start the Application

```bash
cd /root/CascadeProjects/DoganSystem/src/DoganSystem.Web.Mvc
dotnet run
```

Or use the deployment script:
```bash
cd /root/CascadeProjects/DoganSystem
./deploy-all.sh local
```

### Step 2: Access the UI

Once the application starts, you'll see:
```
Now listening on: https://localhost:5001
Now listening on: http://localhost:5000
```

**Access URLs:**
- **Main UI**: http://localhost:5000
- **HTTPS UI**: https://localhost:5001
- **Swagger API**: https://localhost:5001/swagger

---

## 🎯 Available Pages

### Public Pages (No Login Required)
- `/` - Landing page
- `/Public` - Public homepage
- `/Public/About` - About page
- `/Public/Services` - Services page
- `/Public/Pricing` - Pricing page
- `/Public/Contact` - Contact page

### Authenticated Pages (Login Required)
- `/Home` - Dashboard
- `/Tenants` - Tenant management
- `/Agents` - Agent management
- `/ErpNext` - ERPNext instances
- `/Subscriptions` - Subscription management

### GRC Menu (After Login)
The Arabic menu with 19 items will appear after login:
- الصفحة الرئيسية (`/`)
- لوحة التحكم (`/dashboard`)
- الاشتراكات (`/subscriptions`)
- الإدارة (`/admin`)
- مكتبة الأطر التنظيمية (`/frameworks`)
- ... and 14 more items

---

## 🔐 First Time Setup

### 1. Database Migration

If this is the first run, create the database:

```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef database update --startup-project ../DoganSystem.Web.Mvc
```

### 2. Default User

The application uses ABP Identity. You may need to:
1. Register a new user at `/Account/Register`
2. Or use ABP's default admin user (if configured)

### 3. GRC Roles

GRC roles are automatically seeded on first run via `GrcRoleDataSeedContributor`.

---

## 🐛 Troubleshooting

### Application Won't Start

1. **Check .NET SDK**: `dotnet --version` (should be 8.0+)
2. **Restore packages**: `dotnet restore`
3. **Check database**: Ensure SQLite file is writable or SQL Server is accessible
4. **Check ports**: Ensure ports 5000/5001 are not in use

### UI Not Showing

1. **Check if app is running**: Look for "Now listening on" message
2. **Check browser**: Try different browser or incognito mode
3. **Check logs**: Look for errors in console output
4. **Check routes**: Try accessing `/swagger` to verify API is working

### Menu Not Appearing

1. **Login required**: Menu items require authentication
2. **Permissions**: User needs appropriate permissions
3. **Check menu contributor**: Verify `GrcMenuContributor` is in `DoganSystem.Application` project
4. **Check ABP discovery**: ABP should auto-discover menu contributors

---

## 📝 Notes

- The application uses **ABP Framework** with **MVC Razor Views**
- Menu items are **permission-based** - they only show if user has permission
- **Arabic menu** is configured via `GrcMenuContributor`
- **Public pages** don't require authentication
- **GRC pages** require login and appropriate permissions

---

## 🎉 Ready to Use!

Start the application and access the UI at http://localhost:5000
