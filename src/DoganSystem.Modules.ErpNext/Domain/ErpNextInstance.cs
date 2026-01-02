using DoganSystem.Core.Domain.Entities;
using System;
using System.ComponentModel.DataAnnotations;

namespace DoganSystem.Modules.ErpNext.Domain
{
    public class ErpNextInstance : BaseEntity<Guid>
    {
        [Required]
        [MaxLength(256)]
        public string Name { get; set; }

        [Required]
        [MaxLength(512)]
        public string BaseUrl { get; set; }

        [MaxLength(256)]
        public string ApiKey { get; set; }

        [MaxLength(256)]
        public string ApiSecret { get; set; }

        [MaxLength(256)]
        public string SiteName { get; set; }

        public bool IsActive { get; set; }

        public Guid? TenantId { get; set; }

        [MaxLength(1000)]
        public string Description { get; set; }

        public DateTime? LastSyncTime { get; set; }

        public ErpNextInstance()
        {
            IsActive = true;
            CreationTime = DateTime.UtcNow;
        }
    }
}
