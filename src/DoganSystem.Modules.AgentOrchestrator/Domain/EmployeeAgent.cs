using DoganSystem.Core.Domain.Entities;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace DoganSystem.Modules.AgentOrchestrator.Domain
{
    public class EmployeeAgent : BaseEntity<Guid>
    {
        [Required]
        public Guid TenantId { get; set; }

        [Required]
        [MaxLength(256)]
        public string EmployeeName { get; set; }

        [Required]
        [MaxLength(100)]
        public string Role { get; set; }

        [MaxLength(100)]
        public string Department { get; set; }

        public Guid? TeamId { get; set; }

        public Guid? ManagerId { get; set; }

        [MaxLength(50)]
        public string Status { get; set; } // Available, Busy, Away, Offline

        [MaxLength(1000)]
        public string Capabilities { get; set; } // JSON array string

        [MaxLength(256)]
        public string ApiKey { get; set; }

        [MaxLength(512)]
        public string PythonServiceUrl { get; set; } // URL to Python orchestrator service

        public EmployeeAgent()
        {
            Status = "Available";
            CreationTime = DateTime.UtcNow;
        }
    }
}
