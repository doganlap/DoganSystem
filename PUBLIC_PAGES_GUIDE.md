# 🌐 Public Pages Guide - Seamless ABP Integration

## Overview

This guide shows how to create **public pages** (landing pages, marketing pages) that integrate seamlessly with ABP Framework using **MVC Razor Views** (current setup) or **Blazor** (optional).

---

## 🎯 Current Setup: MVC (Razor Views)

### ✅ What We Have:
- **ABP MVC Application** - Using Razor Views
- **Bootstrap 5** - UI framework
- **Arabic Support** - RTL layout

### 📁 Current Structure:
```
src/DoganSystem.Web.Mvc/
├── Controllers/
│   └── HomeController.cs
├── Views/
│   ├── Home/
│   │   └── Index.cshtml
│   └── Shared/
│       └── _Layout.cshtml
└── wwwroot/
    └── css/
```

---

## ✅ Option 1: Public Pages with MVC (Recommended - Current Setup)

### Step 1: Create Public Controller

Create a new controller for public pages:

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    [AllowAnonymous] // Make all actions public
    public class PublicController : AbpController
    {
        // Landing Page
        public IActionResult Index()
        {
            return View();
        }

        // About Page
        public IActionResult About()
        {
            return View();
        }

        // Services Page
        public IActionResult Services()
        {
            return View();
        }

        // Contact Page
        public IActionResult Contact()
        {
            return View();
        }

        // Pricing Page
        public IActionResult Pricing()
        {
            return View();
        }

        // Features Page
        public IActionResult Features()
        {
            return View();
        }
    }
}
```

### Step 2: Create Public Layout (Optional)

Create a separate layout for public pages:

**Views/Shared/_PublicLayout.cshtml:**
```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@ViewData["Title"] - DoganSystem</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
    <link rel="stylesheet" href="~/css/public.css" />
</head>
<body>
    <!-- Public Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-cube"></i> DoganSystem
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">الرئيسية</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/Public/Features">المميزات</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/Public/Pricing">الأسعار</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/Public/About">من نحن</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/Public/Contact">اتصل بنا</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-primary text-white ms-2" href="/Account/Login">تسجيل الدخول</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main>
        @RenderBody()
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white mt-5 py-4">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <h5>DoganSystem</h5>
                    <p>منصة SaaS متعددة المستأجرين مع تكامل ERPNext</p>
                </div>
                <div class="col-md-4">
                    <h5>روابط سريعة</h5>
                    <ul class="list-unstyled">
                        <li><a href="/Public/Features" class="text-white-50">المميزات</a></li>
                        <li><a href="/Public/Pricing" class="text-white-50">الأسعار</a></li>
                        <li><a href="/Public/About" class="text-white-50">من نحن</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>اتصل بنا</h5>
                    <p class="text-white-50">info@dogansystem.com</p>
                </div>
            </div>
            <hr class="bg-white" />
            <div class="text-center">
                <p>&copy; 2025 DoganSystem. جميع الحقوق محفوظة.</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    @await RenderSectionAsync("Scripts", required: false)
</body>
</html>
```

### Step 3: Create Public Views

**Views/Public/Index.cshtml** (Landing Page):
```html
@{
    ViewData["Title"] = "DoganSystem - منصة SaaS متعددة المستأجرين";
    Layout = "~/Views/Shared/_PublicLayout.cshtml";
}

<section class="hero-section bg-primary text-white py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold">مرحباً بك في DoganSystem</h1>
                <p class="lead">منصة SaaS متعددة المستأجرين مع تكامل ERPNext ووكلاء ذكيين</p>
                <div class="mt-4">
                    <a href="/Public/Pricing" class="btn btn-light btn-lg me-2">ابدأ الآن</a>
                    <a href="/Public/Features" class="btn btn-outline-light btn-lg">اعرف المزيد</a>
                </div>
            </div>
            <div class="col-lg-6">
                <img src="~/images/dashboard-preview.png" class="img-fluid" alt="Dashboard Preview" />
            </div>
        </div>
    </div>
</section>

<section class="features-section py-5">
    <div class="container">
        <div class="row text-center mb-5">
            <div class="col-12">
                <h2>المميزات الرئيسية</h2>
                <p class="text-muted">كل ما تحتاجه لإدارة عملك بكفاءة</p>
            </div>
        </div>
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-users fa-3x text-primary mb-3"></i>
                        <h5>إدارة متعددة المستأجرين</h5>
                        <p>عزل كامل للبيانات وإدارة متقدمة للعملاء</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-plug fa-3x text-success mb-3"></i>
                        <h5>تكامل ERPNext</h5>
                        <p>إدارة مثيلات ERPNext متعددة بسهولة</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-robot fa-3x text-info mb-3"></i>
                        <h5>وكلاء ذكيون</h5>
                        <p>وكلاء AI لأتمتة العمليات</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
```

**Views/Public/Pricing.cshtml:**
```html
@{
    ViewData["Title"] = "الأسعار - DoganSystem";
    Layout = "~/Views/Shared/_PublicLayout.cshtml";
}

<section class="pricing-section py-5">
    <div class="container">
        <div class="row text-center mb-5">
            <div class="col-12">
                <h2>خطط الاشتراك</h2>
                <p class="text-muted">اختر الخطة المناسبة لك</p>
            </div>
        </div>
        <div class="row">
            <!-- Starter Plan -->
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white text-center">
                        <h4>Starter</h4>
                        <h2>$99<small>/شهر</small></h2>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success"></i> حتى 10 مستأجرين</li>
                            <li><i class="fas fa-check text-success"></i> 5 وكلاء</li>
                            <li><i class="fas fa-check text-success"></i> دعم أساسي</li>
                        </ul>
                        <a href="/Account/Register" class="btn btn-primary w-100">ابدأ الآن</a>
                    </div>
                </div>
            </div>
            <!-- Professional Plan -->
            <div class="col-md-4 mb-4">
                <div class="card h-100 border-primary">
                    <div class="card-header bg-success text-white text-center">
                        <h4>Professional</h4>
                        <h2>$299<small>/شهر</small></h2>
                        <span class="badge bg-light text-dark">الأكثر شعبية</span>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success"></i> حتى 50 مستأجر</li>
                            <li><i class="fas fa-check text-success"></i> 20 وكيل</li>
                            <li><i class="fas fa-check text-success"></i> دعم متقدم</li>
                        </ul>
                        <a href="/Account/Register" class="btn btn-success w-100">ابدأ الآن</a>
                    </div>
                </div>
            </div>
            <!-- Enterprise Plan -->
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-dark text-white text-center">
                        <h4>Enterprise</h4>
                        <h2>$999<small>/شهر</small></h2>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success"></i> مستأجرون غير محدودين</li>
                            <li><i class="fas fa-check text-success"></i> وكلاء غير محدودين</li>
                            <li><i class="fas fa-check text-success"></i> دعم 24/7</li>
                        </ul>
                        <a href="/Public/Contact" class="btn btn-dark w-100">اتصل بنا</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
```

### Step 4: Configure Routes (Optional)

**Startup.cs or Program.cs:**
```csharp
app.MapControllerRoute(
    name: "public",
    pattern: "{action}",
    defaults: new { controller = "Public", action = "Index" }
);
```

---

## 🔵 Option 2: Add Blazor Support (Optional)

If you want to use Blazor for public pages, you need to add Blazor Server or Blazor WebAssembly.

### Step 1: Add Blazor Package

**DoganSystem.Web.Mvc.csproj:**
```xml
<ItemGroup>
  <PackageReference Include="Volo.Abp.AspNetCore.Mvc.UI.Blazor" Version="8.3.4" />
</ItemGroup>
```

### Step 2: Configure Blazor in Module

**DoganSystemWebMvcModule.cs:**
```csharp
public override void ConfigureServices(ServiceConfigurationContext context)
{
    // ... existing code ...
    
    // Add Blazor Server
    context.Services.AddServerSideBlazor();
}

public override void OnApplicationInitialization(ApplicationInitializationContext context)
{
    var app = context.GetApplicationBuilder();
    
    // ... existing middleware ...
    
    // Add Blazor Hub
    app.MapBlazorHub();
    app.MapFallbackToPage("/_Host");
}
```

### Step 3: Create Blazor Public Page

**Pages/PublicLanding.razor:**
```razor
@page "/"
@layout PublicLayout
@using Volo.Abp.AspNetCore.Components

<PageTitle>DoganSystem - منصة SaaS</PageTitle>

<div class="hero-section">
    <h1>مرحباً بك في DoganSystem</h1>
    <p>منصة SaaS متعددة المستأجرين</p>
    <button class="btn btn-primary" @onclick="NavigateToPricing">ابدأ الآن</button>
</div>

@code {
    [Inject] NavigationManager Navigation { get; set; }
    
    private void NavigateToPricing()
    {
        Navigation.NavigateTo("/pricing");
    }
}
```

---

## ✅ Recommended Approach: MVC (Current Setup)

### Why MVC is Better for Public Pages:

1. ✅ **SEO Friendly** - Server-rendered HTML
2. ✅ **Fast Loading** - No JavaScript bundle needed
3. ✅ **Simple** - Works with current ABP setup
4. ✅ **No Additional Dependencies** - Already configured

### Structure:

```
src/DoganSystem.Web.Mvc/
├── Controllers/
│   └── PublicController.cs          ← Public pages controller
├── Views/
│   ├── Public/
│   │   ├── Index.cshtml            ← Landing page
│   │   ├── About.cshtml            ← About page
│   │   ├── Services.cshtml         ← Services page
│   │   ├── Pricing.cshtml          ← Pricing page
│   │   ├── Features.cshtml         ← Features page
│   │   └── Contact.cshtml          ← Contact page
│   └── Shared/
│       └── _PublicLayout.cshtml    ← Public layout
└── wwwroot/
    └── css/
        └── public.css              ← Public pages styles
```

---

## 🔐 Making Pages Public (AllowAnonymous)

### Method 1: Controller Level (All Actions Public)

```csharp
[AllowAnonymous]
public class PublicController : AbpController
{
    // All actions are public
}
```

### Method 2: Action Level (Specific Actions)

```csharp
public class HomeController : AbpController
{
    [AllowAnonymous]
    public IActionResult Index()
    {
        return View();
    }
    
    [Authorize] // Requires authentication
    public IActionResult Dashboard()
    {
        return View();
    }
}
```

### Method 3: Global Configuration (Allow Public by Default)

**DoganSystemWebMvcModule.cs:**
```csharp
public override void ConfigureServices(ServiceConfigurationContext context)
{
    // Configure authorization
    context.Services.Configure<AuthorizationOptions>(options =>
    {
        options.FallbackPolicy = null; // Allow anonymous by default
    });
}
```

---

## 📝 Complete Example: Public Landing Page

### Controller:

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    [AllowAnonymous]
    public class PublicController : AbpController
    {
        private readonly IConfiguration _configuration;

        public PublicController(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        public IActionResult Index()
        {
            ViewBag.AppName = "DoganSystem";
            ViewBag.AppDescription = "منصة SaaS متعددة المستأجرين";
            return View();
        }

        public IActionResult Pricing()
        {
            // You can inject AppServices here if needed
            // var subscriptionService = LazyServiceProvider.LazyGetRequiredService<ISubscriptionAppService>();
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Contact(ContactFormDto input)
        {
            // Process contact form
            // Can use ABP services here
            return Json(new { success = true, message = "تم إرسال الرسالة بنجاح" });
        }
    }
}
```

### View with ABP Integration:

**Views/Public/Index.cshtml:**
```html
@using Volo.Abp.AspNetCore.Mvc.UI.Theming
@inject IThemeManager ThemeManager
@{
    ViewData["Title"] = "DoganSystem - منصة SaaS";
    Layout = "~/Views/Shared/_PublicLayout.cshtml";
}

<section class="hero bg-primary text-white py-5">
    <div class="container">
        <h1>@ViewBag.AppName</h1>
        <p>@ViewBag.AppDescription</p>
        
        <!-- Use ABP localization if needed -->
        <a href="/Public/Pricing" class="btn btn-light">ابدأ الآن</a>
    </div>
</section>

<!-- Features section can use ABP services via AJAX -->
<section class="features py-5">
    <div class="container">
        <div id="features-list">
            <!-- Loaded via AJAX from API -->
        </div>
    </div>
</section>

@section Scripts {
    <script>
        // Call ABP API endpoints
        fetch('/api/subscriptions')
            .then(r => r.json())
            .then(data => {
                // Display pricing plans
            });
    </script>
}
```

---

## 🔗 Integration with ABP Services

### Accessing ABP Services in Public Pages:

```csharp
[AllowAnonymous]
public class PublicController : AbpController
{
    // Inject ABP services
    private readonly ISubscriptionAppService _subscriptionService;
    
    public PublicController(ISubscriptionAppService subscriptionService)
    {
        _subscriptionService = subscriptionService;
    }
    
    public async Task<IActionResult> Pricing()
    {
        // Use ABP service to get subscription plans
        var plans = new[]
        {
            new { Name = "Starter", Price = 99 },
            new { Name = "Professional", Price = 299 },
            new { Name = "Enterprise", Price = 999 }
        };
        
        ViewBag.Plans = plans;
        return View();
    }
}
```

---

## 🎨 Styling Public Pages

### Create Public CSS:

**wwwroot/css/public.css:**
```css
/* Public pages specific styles */
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 500px;
    display: flex;
    align-items: center;
}

.features-section .card {
    transition: transform 0.3s;
}

.features-section .card:hover {
    transform: translateY(-5px);
}

/* RTL Support */
[dir="rtl"] .navbar-nav {
    margin-right: 0;
    margin-left: auto;
}
```

---

## 📊 Summary

### ✅ Recommended: MVC Razor Views

**Advantages:**
- ✅ Works with current ABP setup
- ✅ SEO friendly
- ✅ Fast loading
- ✅ Simple implementation
- ✅ Full ABP integration

**Structure:**
```
PublicController (AllowAnonymous)
    ├── Index (Landing)
    ├── About
    ├── Services
    ├── Pricing
    ├── Features
    └── Contact
```

### 🔵 Optional: Blazor

**When to Use:**
- If you need interactive components
- If you prefer component-based architecture
- If you want to share components with admin pages

**Requirements:**
- Add Blazor package
- Configure Blazor Hub
- Create Blazor components

---

## 🚀 Quick Start

1. **Create PublicController** with `[AllowAnonymous]`
2. **Create Views** in `Views/Public/`
3. **Create Public Layout** in `Views/Shared/_PublicLayout.cshtml`
4. **Add Routes** (optional, defaults work)
5. **Style** with `wwwroot/css/public.css`

**Result:** Public pages seamlessly integrated with ABP! ✅

---

**Last Updated:** 2025-01-22
