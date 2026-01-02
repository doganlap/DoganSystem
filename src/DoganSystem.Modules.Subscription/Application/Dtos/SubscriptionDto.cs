using System;
using System.ComponentModel.DataAnnotations;
using Volo.Abp.Application.Dtos;

namespace DoganSystem.Modules.Subscription.Application.Dtos
{
    public class SubscriptionDto : EntityDto<Guid>
    {
        public Guid TenantId { get; set; }
        public string PlanType { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string Status { get; set; }
        public decimal MonthlyPrice { get; set; }
        public string PaymentProvider { get; set; }
        public string PaymentProviderSubscriptionId { get; set; }
        public DateTime? NextBillingDate { get; set; }
        public DateTime CreationTime { get; set; }
    }

    public class CreateSubscriptionDto
    {
        [Required]
        public Guid TenantId { get; set; }

        [Required]
        [StringLength(50)]
        public string PlanType { get; set; }

        public DateTime? StartDate { get; set; }

        public DateTime? EndDate { get; set; }

        [StringLength(256)]
        public string PaymentProvider { get; set; }

        [StringLength(256)]
        public string PaymentProviderSubscriptionId { get; set; }
    }

    public class UpdateSubscriptionDto
    {
        [StringLength(50)]
        public string PlanType { get; set; }

        [StringLength(50)]
        public string Status { get; set; }

        public DateTime? EndDate { get; set; }

        public decimal? MonthlyPrice { get; set; }
    }

    public class SubscriptionListDto : PagedAndSortedResultRequestDto
    {
        public Guid? TenantId { get; set; }
        public string Status { get; set; }
        public string PlanType { get; set; }
    }
}
