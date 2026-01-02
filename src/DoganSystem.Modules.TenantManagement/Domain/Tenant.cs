using DoganSystem.Core.Domain.Entities;
using System;
using System.ComponentModel.DataAnnotations;

namespace DoganSystem.Modules.TenantManagement.Domain
{
    public class Tenant : BaseEntity<Guid>
    {
        [Required]
        [MaxLength(256)]
        public string Name { get; set; }

        [MaxLength(100)]
        public string Subdomain { get; set; }

        [MaxLength(256)]
        public string Domain { get; set; }

        [Required]
        [MaxLength(50)]
        public string Status { get; set; } // Active, Suspended, Cancelled, Trial

        [Required]
        [MaxLength(50)]
        public string SubscriptionTier { get; set; } // Starter, Professional, Enterprise

        public DateTime? TrialEndDate { get; set; }

        public Guid? ErpNextInstanceId { get; set; }

        [MaxLength(1000)]
        public string Metadata { get; set; } // JSON string

        public Tenant()
        {
            Status = "Trial";
            SubscriptionTier = "Starter";
            CreationTime = DateTime.UtcNow;
        }
    }
}
