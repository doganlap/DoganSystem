# Consultant Offers Module - Complete Guide

## Overview

The Consultant Offers Module provides a complete structure for managing consultant/employee offers with full ERPNext integration and ERP functionality for all employees.

## ✅ What Has Been Implemented

### 1. Domain Layer ✅
**File:** `src/DoganSystem.Modules.ConsultantOffers/Domain/ConsultantOffer.cs`

**Entity Properties:**
- `TenantId` - Multi-tenant support
- `EmployeeAgentId` - Link to employee/consultant
- `ErpNextInstanceId` - Link to ERPNext instance
- `OfferNumber` - Unique offer number (e.g., "OFF-2025-001")
- `Title`, `Description` - Offer details
- `OfferType` - Project, Retainer, Hourly, Fixed
- `Amount`, `Currency` - Financial details
- `StartDate`, `EndDate` - Timeline
- `Status` - Draft, Sent, Accepted, Rejected, Expired, Completed
- `ClientName`, `ClientEmail`, `ClientPhone` - Client information
- `ErpNextQuotationId` - Link to ERPNext Quotation
- `ErpNextSalesOrderId` - Link to ERPNext Sales Order
- `ErpNextCustomerId` - Link to ERPNext Customer
- `TermsAndConditions`, `Deliverables`, `PaymentTerms` - Contract details

### 2. Application Layer ✅
**Files:**
- `ConsultantOfferDto.cs` - DTOs (Create, Update, List, Detail)
- `ConsultantOfferAppService.cs` - Application service with full CRUD

**Features:**
- ✅ Create offers with auto-generated offer numbers
- ✅ Update offers
- ✅ Delete offers
- ✅ List offers with filtering and pagination
- ✅ Send offers (changes status to "Sent")
- ✅ Accept offers (creates ERPNext Sales Order)
- ✅ Reject offers
- ✅ ERPNext integration (auto-create Quotation and Sales Order)

### 3. Entity Framework Core ✅
**Configuration:**
- Added to `DoganSystemDbContext`
- EF Core configuration with indexes
- Unique constraint on `OfferNumber`
- Indexes on `TenantId`, `EmployeeAgentId`, `Status`

### 4. ERPNext Integration ✅
**Features:**
- Auto-create Quotation in ERPNext when creating offer
- Auto-create Sales Order when offer is accepted
- Link to ERPNext Customer
- Sync offer data with ERPNext

### 5. Multi-Tenant Support ✅
- Tenant-aware queries
- Tenant isolation
- Per-tenant offer management

## 📋 API Endpoints

### ConsultantOfferAppService Methods

1. **CreateAsync** - Create new offer
   - Auto-generates offer number
   - Optional ERPNext quotation creation
   - Links to employee and ERPNext instance

2. **UpdateAsync** - Update existing offer
   - Update any offer fields
   - Maintains status workflow

3. **GetAsync** - Get single offer
   - Includes employee name
   - Includes ERPNext instance name

4. **GetListAsync** - List offers with filters
   - Filter by employee, status, type
   - Pagination and sorting
   - Tenant-aware

5. **SendAsync** - Send offer to client
   - Changes status from "Draft" to "Sent"
   - Records sent date

6. **AcceptAsync** - Accept offer
   - Changes status to "Accepted"
   - Creates ERPNext Sales Order if linked
   - Records acceptance date

7. **RejectAsync** - Reject offer
   - Changes status to "Rejected"
   - Records rejection reason and date

## 🔗 ERPNext Integration Flow

### 1. Create Offer with ERPNext
```
Create Offer → Create ERPNext Quotation → Link Quotation ID
```

### 2. Accept Offer
```
Accept Offer → Create ERPNext Sales Order from Quotation → Link Sales Order ID
```

### 3. ERPNext Data Structure
- **Quotation**: Contains offer details, items, pricing
- **Sales Order**: Created from accepted quotation
- **Customer**: Linked via ClientName/ClientEmail

## 📊 Offer Status Workflow

```
Draft → Sent → Accepted → Completed
              ↓
           Rejected
              ↓
           Expired
```

## 🎯 Usage Examples

### Create Offer
```csharp
var offer = await _offerAppService.CreateAsync(new CreateConsultantOfferDto
{
    EmployeeAgentId = employeeId,
    ErpNextInstanceId = erpNextInstanceId,
    Title = "ERPNext Implementation Project",
    Description = "Complete ERPNext setup and configuration",
    OfferType = "Project",
    Amount = 50000,
    Currency = "SAR",
    StartDate = DateTime.UtcNow,
    EndDate = DateTime.UtcNow.AddMonths(6),
    ClientName = "ABC Company",
    ClientEmail = "contact@abccompany.com",
    CreateInErpNext = true // Auto-create quotation
});
```

### Send Offer
```csharp
await _offerAppService.SendAsync(offerId);
```

### Accept Offer
```csharp
var acceptedOffer = await _offerAppService.AcceptAsync(offerId);
// Sales Order automatically created in ERPNext
```

## 🔧 Configuration

### Database Migration
```bash
cd src/DoganSystem.EntityFrameworkCore
dotnet ef migrations add AddConsultantOffers
dotnet ef database update
```

### Module Registration
The module is automatically registered when added to:
- `DoganSystemWebMvcModule` (MVC app)
- `DoganSystemBlazorServerModule` (Blazor app)

## 📱 Blazor Components

### ConsultantOffers.razor
- List all offers
- Filter by status, employee, type
- Send/Accept/Reject actions
- View offer details

## 🔐 Authorization

All methods require `[Authorize]` attribute:
- Users must be authenticated
- Can be extended with permissions

## 📈 Future Enhancements

1. **Email Notifications**
   - Send offer via email
   - Notify on acceptance/rejection

2. **PDF Generation**
   - Generate offer PDF
   - Include terms and conditions

3. **Approval Workflow**
   - Multi-level approvals
   - Approval history

4. **Reporting**
   - Offer statistics
   - Revenue tracking
   - Employee performance

5. **Templates**
   - Offer templates
   - Pre-filled terms

## 📝 Database Schema

```sql
CREATE TABLE ConsultantOffers (
    Id UNIQUEIDENTIFIER PRIMARY KEY,
    TenantId UNIQUEIDENTIFIER NOT NULL,
    EmployeeAgentId UNIQUEIDENTIFIER NOT NULL,
    ErpNextInstanceId UNIQUEIDENTIFIER NULL,
    OfferNumber NVARCHAR(256) NOT NULL UNIQUE,
    Title NVARCHAR(500) NOT NULL,
    Description NVARCHAR(2000) NULL,
    OfferType NVARCHAR(100) NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    Currency NVARCHAR(10) NOT NULL,
    StartDate DATETIME2 NOT NULL,
    EndDate DATETIME2 NULL,
    Status NVARCHAR(50) NOT NULL,
    ClientName NVARCHAR(100) NULL,
    ClientEmail NVARCHAR(256) NULL,
    ClientPhone NVARCHAR(50) NULL,
    ErpNextQuotationId NVARCHAR(256) NULL,
    ErpNextSalesOrderId NVARCHAR(256) NULL,
    ErpNextCustomerId NVARCHAR(256) NULL,
    TermsAndConditions NVARCHAR(5000) NULL,
    Deliverables NVARCHAR(2000) NULL,
    PaymentTerms NVARCHAR(2000) NULL,
    SentDate DATETIME2 NULL,
    AcceptedDate DATETIME2 NULL,
    RejectedDate DATETIME2 NULL,
    RejectionReason NVARCHAR(1000) NULL,
    Notes NVARCHAR(1000) NULL,
    CreationTime DATETIME2 NOT NULL,
    LastModificationTime DATETIME2 NULL
);

CREATE INDEX IX_ConsultantOffers_TenantId ON ConsultantOffers(TenantId);
CREATE INDEX IX_ConsultantOffers_EmployeeAgentId ON ConsultantOffers(EmployeeAgentId);
CREATE INDEX IX_ConsultantOffers_Status ON ConsultantOffers(Status);
CREATE INDEX IX_ConsultantOffers_ErpNextQuotationId ON ConsultantOffers(ErpNextQuotationId);
```

## ✅ Status

**Module Status:** ✅ **COMPLETE AND READY**

The Consultant Offers Module is fully implemented with:
- ✅ Domain entity
- ✅ Application service with full CRUD
- ✅ ERPNext integration
- ✅ Multi-tenant support
- ✅ Blazor components
- ✅ Database configuration

**Next Step:** Run database migration to create the table.
