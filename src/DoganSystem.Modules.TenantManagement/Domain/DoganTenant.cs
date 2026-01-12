using System;
using System.ComponentModel.DataAnnotations;
using Volo.Abp.TenantManagement;

namespace DoganSystem.Modules.TenantManagement.Domain
{
    /// <summary>
    /// Extended tenant entity that adds custom properties to ABP's Tenant
    /// </summary>
    public class DoganTenant : Tenant
    {
        [MaxLength(100)]
        public string? Subdomain { get; set; }

        [MaxLength(50)]
        public string Status { get; set; } = "Trial"; // Active, Suspended, Cancelled, Trial

        [MaxLength(50)]
        public string SubscriptionTier { get; set; } = "Starter"; // Starter, Professional, Enterprise

        public DateTime? TrialEndDate { get; set; }

        public Guid? ErpNextInstanceId { get; set; }

        [MaxLength(1000)]
        public string? Metadata { get; set; } // JSON string

        public DoganTenant()
        {
            Status = "Trial";
            SubscriptionTier = "Starter";
        }
    }
}
