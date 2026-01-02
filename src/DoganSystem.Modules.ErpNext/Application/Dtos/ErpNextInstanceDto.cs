using System;
using System.ComponentModel.DataAnnotations;
using Volo.Abp.Application.Dtos;

namespace DoganSystem.Modules.ErpNext.Application.Dtos
{
    public class ErpNextInstanceDto : EntityDto<Guid>
    {
        public string Name { get; set; }
        public string BaseUrl { get; set; }
        public string ApiKey { get; set; }
        public string ApiSecret { get; set; }
        public string SiteName { get; set; }
        public bool IsActive { get; set; }
        public Guid? TenantId { get; set; }
        public string Description { get; set; }
        public DateTime? LastSyncTime { get; set; }
        public DateTime CreationTime { get; set; }
    }

    public class CreateErpNextInstanceDto
    {
        [Required]
        [StringLength(256)]
        public string Name { get; set; }

        [Required]
        [StringLength(512)]
        [Url]
        public string BaseUrl { get; set; }

        [StringLength(256)]
        public string ApiKey { get; set; }

        [StringLength(256)]
        public string ApiSecret { get; set; }

        [StringLength(256)]
        public string SiteName { get; set; }

        public Guid? TenantId { get; set; }

        [StringLength(1000)]
        public string Description { get; set; }
    }

    public class UpdateErpNextInstanceDto
    {
        [StringLength(256)]
        public string Name { get; set; }

        [StringLength(512)]
        [Url]
        public string BaseUrl { get; set; }

        [StringLength(256)]
        public string ApiKey { get; set; }

        [StringLength(256)]
        public string ApiSecret { get; set; }

        [StringLength(256)]
        public string SiteName { get; set; }

        public bool? IsActive { get; set; }

        [StringLength(1000)]
        public string Description { get; set; }
    }

    public class ErpNextInstanceListDto : PagedAndSortedResultRequestDto
    {
        public string Filter { get; set; }
        public Guid? TenantId { get; set; }
        public bool? IsActive { get; set; }
    }
}
