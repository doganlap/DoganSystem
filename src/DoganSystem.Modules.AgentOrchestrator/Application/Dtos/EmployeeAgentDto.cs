using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using Volo.Abp.Application.Dtos;

namespace DoganSystem.Modules.AgentOrchestrator.Application.Dtos
{
    public class EmployeeAgentDto : EntityDto<Guid>
    {
        public Guid TenantId { get; set; }
        public string EmployeeName { get; set; }
        public string Role { get; set; }
        public string Department { get; set; }
        public Guid? TeamId { get; set; }
        public Guid? ManagerId { get; set; }
        public string Status { get; set; }
        public List<string> Capabilities { get; set; }
        public string ApiKey { get; set; }
        public string PythonServiceUrl { get; set; }
        public DateTime CreationTime { get; set; }
    }

    public class CreateEmployeeAgentDto
    {
        [Required]
        public Guid TenantId { get; set; }

        [Required]
        [StringLength(256)]
        public string EmployeeName { get; set; }

        [Required]
        [StringLength(100)]
        public string Role { get; set; }

        [StringLength(100)]
        public string Department { get; set; }

        public Guid? TeamId { get; set; }

        public Guid? ManagerId { get; set; }

        public List<string> Capabilities { get; set; }
    }

    public class UpdateEmployeeAgentDto
    {
        [StringLength(256)]
        public string EmployeeName { get; set; }

        [StringLength(100)]
        public string Role { get; set; }

        [StringLength(100)]
        public string Department { get; set; }

        public Guid? TeamId { get; set; }

        public Guid? ManagerId { get; set; }

        [StringLength(50)]
        public string Status { get; set; }

        public List<string> Capabilities { get; set; }
    }

    public class EmployeeAgentListDto : PagedAndSortedResultRequestDto
    {
        public Guid? TenantId { get; set; }
        public string Filter { get; set; }
        public string Status { get; set; }
        public string Department { get; set; }
    }
}
