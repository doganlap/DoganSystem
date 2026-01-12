using Microsoft.EntityFrameworkCore;
using Volo.Abp.Data;
using Volo.Abp.EntityFrameworkCore;
using Volo.Abp.Identity.EntityFrameworkCore;
using Volo.Abp.TenantManagement.EntityFrameworkCore;
using Volo.Abp.PermissionManagement.EntityFrameworkCore;
using Volo.Abp.FeatureManagement.EntityFrameworkCore;
// using Volo.Abp.OpenIddict.EntityFrameworkCore;
using DoganSystem.Modules.ErpNext.Domain;
using DoganSystem.Modules.AgentOrchestrator.Domain;
using DoganSystem.Modules.Subscription.Domain;
using DoganSystem.Core.Domain.Entities;
using SubscriptionEntity = DoganSystem.Modules.Subscription.Domain.Subscription;

namespace DoganSystem.EntityFrameworkCore
{
    [ConnectionStringName("Default")]
    public class DoganSystemDbContext : AbpDbContext<DoganSystemDbContext>
    {
        // ERPNext Module
        public DbSet<ErpNextInstance> ErpNextInstances { get; set; }

        // Agent Orchestrator Module
        public DbSet<EmployeeAgent> EmployeeAgents { get; set; }

        // Subscription Module
        public DbSet<SubscriptionEntity> Subscriptions { get; set; }

        // Contact Submissions from Landing Pages
        public DbSet<ContactSubmission> ContactSubmissions { get; set; }

        public DoganSystemDbContext(DbContextOptions<DoganSystemDbContext> options)
            : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);

            // Configure ABP Identity entities
            builder.ConfigureIdentity();

            // Configure ABP TenantManagement entities
            builder.ConfigureTenantManagement();

            // Configure ABP PermissionManagement entities
            builder.ConfigurePermissionManagement();

            // Configure ABP FeatureManagement entities
            builder.ConfigureFeatureManagement();

            // OpenIddict configuration temporarily disabled
            // builder.ConfigureOpenIddict();

            // Configure custom entities
            builder.ConfigureDoganSystem();
        }
    }
}
