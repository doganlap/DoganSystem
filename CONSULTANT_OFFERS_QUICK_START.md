# Consultant Offers Module - Quick Start

## ✅ Module Complete

The Consultant Offers Module provides a complete structure for managing consultant/employee offers with ERPNext integration.

## 🚀 Quick Setup

### 1. Run Database Migration

```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add AddConsultantOffers
dotnet ef database update
```

### 2. Use in Application

**MVC Application:**
- Module automatically registered
- Access via API endpoints

**Blazor Application:**
- Module automatically registered
- Access via `ConsultantOffers.razor` page

## 📋 Key Features

1. **Offer Management**
   - Create offers for any employee
   - Auto-generated offer numbers (OFF-2025-001, etc.)
   - Full CRUD operations

2. **ERPNext Integration**
   - Auto-create Quotation in ERPNext
   - Auto-create Sales Order on acceptance
   - Link to ERPNext Customer

3. **Status Workflow**
   - Draft → Sent → Accepted/Rejected
   - Track all status changes

4. **Multi-Tenant**
   - Tenant-aware queries
   - Per-tenant offer management

## 📝 Example Usage

```csharp
// Create offer
var offer = await _offerAppService.CreateAsync(new CreateConsultantOfferDto
{
    EmployeeAgentId = employeeId,
    ErpNextInstanceId = erpNextInstanceId,
    Title = "ERPNext Implementation",
    OfferType = "Project",
    Amount = 50000,
    Currency = "SAR",
    StartDate = DateTime.UtcNow,
    CreateInErpNext = true
});

// Send offer
await _offerAppService.SendAsync(offer.Id);

// Accept offer (creates Sales Order in ERPNext)
await _offerAppService.AcceptAsync(offer.Id);
```

## 🔗 Integration Points

- **Employee Agents** - Links offers to employees
- **ERPNext** - Creates quotations and sales orders
- **Tenants** - Multi-tenant support

**Status:** ✅ **READY TO USE**
