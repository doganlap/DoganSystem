using System;
using System.ComponentModel.DataAnnotations;
using Volo.Abp.Application.Dtos;

namespace DoganSystem.Modules.TenantManagement.Application.Dtos
{
    public class TenantDto : EntityDto<Guid>
    {
        public string Name { get; set; } = string.Empty;
        public string Subdomain { get; set; } = string.Empty;
        public string Domain { get; set; } = string.Empty;
        public string Status { get; set; } = string.Empty;
        public string SubscriptionTier { get; set; } = string.Empty;
        public DateTime? TrialEndDate { get; set; }
        public Guid? ErpNextInstanceId { get; set; }
        public string? Metadata { get; set; }
        public DateTime CreationTime { get; set; }
        public DateTime? LastModificationTime { get; set; }
    }

    public class CreateTenantDto
    {
        [Required]
        [StringLength(256)]
        public string Name { get; set; } = string.Empty;

        [StringLength(100)]
        public string Subdomain { get; set; } = string.Empty;

        [StringLength(256)]
        public string Domain { get; set; } = string.Empty;

        [StringLength(50)]
        public string SubscriptionTier { get; set; } = "Starter";

        public int TrialDays { get; set; } = 14;

        [StringLength(1000)]
        public string? Metadata { get; set; }
    }

    public class UpdateTenantDto
    {
        [StringLength(256)]
        public string? Name { get; set; }

        [StringLength(256)]
        public string? Domain { get; set; }

        [StringLength(50)]
        public string? Status { get; set; }

        [StringLength(50)]
        public string? SubscriptionTier { get; set; }

        [StringLength(1000)]
        public string? Metadata { get; set; }
    }

    public class TenantListDto : PagedAndSortedResultRequestDto
    {
        public string? Filter { get; set; }
        public string? Status { get; set; }
        public string? SubscriptionTier { get; set; }
    }
}
