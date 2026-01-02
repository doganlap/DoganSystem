using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.AgentOrchestrator.Domain;
using Volo.Abp.Data;
using Volo.Abp.EntityFrameworkCore;

namespace DoganSystem.Modules.AgentOrchestrator.EntityFrameworkCore
{
    [ConnectionStringName("Default")]
    public class AgentOrchestratorDbContext : AbpDbContext<AgentOrchestratorDbContext>
    {
        public DbSet<EmployeeAgent> EmployeeAgents { get; set; }

        public AgentOrchestratorDbContext(DbContextOptions<AgentOrchestratorDbContext> options)
            : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);
            builder.ConfigureAgentOrchestrator();
        }
    }
}
