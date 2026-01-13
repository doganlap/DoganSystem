using DoganSystem.Core.Domain.Entities;
using System;
using System.ComponentModel.DataAnnotations;

namespace DoganSystem.Modules.ConsultantOffers.Domain
{
    /// <summary>
    /// Consultant offer entity - represents an offer/contract for a consultant/employee
    /// </summary>
    public class ConsultantOffer : BaseEntity<Guid>
    {
        [Required]
        public Guid TenantId { get; set; }

        [Required]
        public Guid EmployeeAgentId { get; set; }

        [Required]
        public Guid? ErpNextInstanceId { get; set; }

        [Required]
        [MaxLength(256)]
        public required string OfferNumber { get; set; } // e.g., "OFF-2025-001"

        [Required]
        [MaxLength(500)]
        public required string Title { get; set; }

        [MaxLength(2000)]
        public string? Description { get; set; }

        [Required]
        [MaxLength(100)]
        public required string OfferType { get; set; } // Project, Retainer, Hourly, Fixed

        [Required]
        public decimal Amount { get; set; }

        [MaxLength(10)]
        public string Currency { get; set; } = "SAR"; // SAR, USD, EUR

        [Required]
        public DateTime StartDate { get; set; }

        public DateTime? EndDate { get; set; }

        [Required]
        [MaxLength(50)]
        public required string Status { get; set; } // Draft, Sent, Accepted, Rejected, Expired, Completed

        [MaxLength(100)]
        public string? ClientName { get; set; }

        [MaxLength(256)]
        public string? ClientEmail { get; set; }

        [MaxLength(50)]
        public string? ClientPhone { get; set; }

        // ERPNext Integration
        [MaxLength(256)]
        public string? ErpNextQuotationId { get; set; } // Link to ERPNext Quotation

        [MaxLength(256)]
        public string? ErpNextSalesOrderId { get; set; } // Link to ERPNext Sales Order

        [MaxLength(256)]
        public string? ErpNextCustomerId { get; set; } // Link to ERPNext Customer

        // Terms and Conditions
        [MaxLength(5000)]
        public string? TermsAndConditions { get; set; }

        [MaxLength(2000)]
        public string? Deliverables { get; set; }

        [MaxLength(2000)]
        public string? PaymentTerms { get; set; }

        // Dates
        public DateTime? SentDate { get; set; }

        public DateTime? AcceptedDate { get; set; }

        public DateTime? RejectedDate { get; set; }

        [MaxLength(1000)]
        public string? RejectionReason { get; set; }

        // Metadata
        [MaxLength(1000)]
        public string? Notes { get; set; }

        [MaxLength(1000)]
        public string? Metadata { get; set; } // JSON for additional data

        public ConsultantOffer()
        {
            Status = "Draft";
            Currency = "SAR";
            CreationTime = DateTime.UtcNow;
        }
    }
}
