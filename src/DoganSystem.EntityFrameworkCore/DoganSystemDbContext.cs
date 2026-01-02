using Microsoft.EntityFrameworkCore;
using Volo.Abp.Data;
using Volo.Abp.EntityFrameworkCore;
using DoganSystem.Modules.ErpNext.Domain;
using DoganSystem.Modules.TenantManagement.Domain;
using DoganSystem.Modules.AgentOrchestrator.Domain;
using DoganSystem.Modules.Subscription.Domain;

namespace DoganSystem.EntityFrameworkCore
{
    [ConnectionStringName("Default")]
    public class DoganSystemDbContext : AbpDbContext<DoganSystemDbContext>
    {
        // ERPNext Module
        public DbSet<ErpNextInstance> ErpNextInstances { get; set; }
        
        // Tenant Management Module
        public DbSet<Tenant> Tenants { get; set; }
        
        // Agent Orchestrator Module
        public DbSet<EmployeeAgent> EmployeeAgents { get; set; }
        
        // Subscription Module
        public DbSet<Subscription> Subscriptions { get; set; }

        public DoganSystemDbContext(DbContextOptions<DoganSystemDbContext> options)
            : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);

            // Configure entities
            builder.ConfigureDoganSystem();
        }
    }
}
