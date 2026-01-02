using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.AgentOrchestrator.Domain;
using Volo.Abp.EntityFrameworkCore.Modeling;

namespace DoganSystem.Modules.AgentOrchestrator.EntityFrameworkCore
{
    public static class AgentOrchestratorDbContextModelCreatingExtensions
    {
        public static void ConfigureAgentOrchestrator(this ModelBuilder builder)
        {
            builder.Entity<EmployeeAgent>(b =>
            {
                b.ToTable("EmployeeAgents");
                b.ConfigureByConvention();
                b.Property(x => x.EmployeeName).IsRequired().HasMaxLength(256);
                b.Property(x => x.Role).IsRequired().HasMaxLength(100);
                b.Property(x => x.Status).IsRequired().HasMaxLength(50);
                b.HasIndex(x => x.TenantId);
                b.HasIndex(x => x.TeamId);
                b.HasIndex(x => x.ManagerId);
            });
        }
    }
}
