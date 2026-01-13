using System;
using Volo.Abp.Application.Dtos;

namespace DoganSystem.Modules.ConsultantOffers.Application.Dtos
{
    public class ConsultantOfferDto
    {
        public Guid Id { get; set; }
        public Guid TenantId { get; set; }
        public Guid EmployeeAgentId { get; set; }
        public string EmployeeName { get; set; } = string.Empty;
        public Guid? ErpNextInstanceId { get; set; }
        public string ErpNextInstanceName { get; set; } = string.Empty;
        public string OfferNumber { get; set; } = string.Empty;
        public string Title { get; set; } = string.Empty;
        public string? Description { get; set; }
        public string OfferType { get; set; } = string.Empty;
        public decimal Amount { get; set; }
        public string Currency { get; set; } = "SAR";
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string Status { get; set; } = string.Empty;
        public string? ClientName { get; set; }
        public string? ClientEmail { get; set; }
        public string? ClientPhone { get; set; }
        public string? ErpNextQuotationId { get; set; }
        public string? ErpNextSalesOrderId { get; set; }
        public string? ErpNextCustomerId { get; set; }
        public string? TermsAndConditions { get; set; }
        public string? Deliverables { get; set; }
        public string? PaymentTerms { get; set; }
        public DateTime? SentDate { get; set; }
        public DateTime? AcceptedDate { get; set; }
        public DateTime? RejectedDate { get; set; }
        public string? RejectionReason { get; set; }
        public string? Notes { get; set; }
        public DateTime CreationTime { get; set; }
        public DateTime? LastModificationTime { get; set; }
    }

    public class CreateConsultantOfferDto
    {
        public Guid EmployeeAgentId { get; set; }
        public Guid? ErpNextInstanceId { get; set; }
        public string Title { get; set; } = string.Empty;
        public string? Description { get; set; }
        public string OfferType { get; set; } = "Project";
        public decimal Amount { get; set; }
        public string Currency { get; set; } = "SAR";
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string? ClientName { get; set; }
        public string? ClientEmail { get; set; }
        public string? ClientPhone { get; set; }
        public string? TermsAndConditions { get; set; }
        public string? Deliverables { get; set; }
        public string? PaymentTerms { get; set; }
        public string? Notes { get; set; }
        public bool CreateInErpNext { get; set; } = false; // Auto-create quotation in ERPNext
    }

    public class UpdateConsultantOfferDto
    {
        public string? Title { get; set; }
        public string? Description { get; set; }
        public string? OfferType { get; set; }
        public decimal? Amount { get; set; }
        public string? Currency { get; set; }
        public DateTime? StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string? Status { get; set; }
        public string? ClientName { get; set; }
        public string? ClientEmail { get; set; }
        public string? ClientPhone { get; set; }
        public string? TermsAndConditions { get; set; }
        public string? Deliverables { get; set; }
        public string? PaymentTerms { get; set; }
        public string? Notes { get; set; }
    }

    public class ConsultantOfferListDto : PagedAndSortedResultRequestDto
    {
        public Guid? EmployeeAgentId { get; set; }
        public Guid? TenantId { get; set; }
        public string? Status { get; set; }
        public string? OfferType { get; set; }
        public string? Filter { get; set; }
    }
}
