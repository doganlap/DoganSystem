using DoganSystem.Core.Domain.Entities;
using System;
using System.ComponentModel.DataAnnotations;

namespace DoganSystem.Modules.Subscription.Domain
{
    public class Subscription : BaseEntity<Guid>
    {
        [Required]
        public Guid TenantId { get; set; }

        [Required]
        [MaxLength(50)]
        public string PlanType { get; set; } // Starter, Professional, Enterprise

        [Required]
        public DateTime StartDate { get; set; }

        public DateTime? EndDate { get; set; }

        [Required]
        [MaxLength(50)]
        public string Status { get; set; } // Active, Cancelled, Expired, Suspended

        public decimal MonthlyPrice { get; set; }

        [MaxLength(256)]
        public string PaymentProvider { get; set; } // Stripe, etc.

        [MaxLength(256)]
        public string PaymentProviderSubscriptionId { get; set; }

        public DateTime? NextBillingDate { get; set; }

        public Subscription()
        {
            Status = "Active";
            CreationTime = DateTime.UtcNow;
            StartDate = DateTime.UtcNow;
        }
    }
}
