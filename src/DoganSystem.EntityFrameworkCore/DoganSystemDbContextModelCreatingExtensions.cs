using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.ErpNext.Domain;
using DoganSystem.Modules.TenantManagement.Domain;
using DoganSystem.Modules.AgentOrchestrator.Domain;
using DoganSystem.Modules.Subscription.Domain;
using Volo.Abp.EntityFrameworkCore.Modeling;

namespace DoganSystem.EntityFrameworkCore
{
    public static class DoganSystemDbContextModelCreatingExtensions
    {
        public static void ConfigureDoganSystem(this ModelBuilder builder)
        {
            // Configure ERPNext module
            builder.Entity<ErpNextInstance>(b =>
            {
                b.ToTable("ErpNextInstances");
                b.ConfigureByConvention();
                b.Property(x => x.Name).IsRequired().HasMaxLength(256);
                b.Property(x => x.BaseUrl).IsRequired().HasMaxLength(512);
                b.HasIndex(x => x.TenantId);
            });
            
            // Configure Tenant Management module
            builder.Entity<Tenant>(b =>
            {
                b.ToTable("Tenants");
                b.ConfigureByConvention();
                b.Property(x => x.Name).IsRequired().HasMaxLength(256);
                b.Property(x => x.Status).IsRequired().HasMaxLength(50);
                b.Property(x => x.SubscriptionTier).IsRequired().HasMaxLength(50);
                b.HasIndex(x => x.Subdomain).IsUnique();
                b.HasIndex(x => x.Domain);
            });
            
            // Configure Agent Orchestrator module
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
            
            // Configure Subscription module
            builder.Entity<Subscription>(b =>
            {
                b.ToTable("Subscriptions");
                b.ConfigureByConvention();
                b.Property(x => x.PlanType).IsRequired().HasMaxLength(50);
                b.Property(x => x.Status).IsRequired().HasMaxLength(50);
                b.HasIndex(x => x.TenantId);
                b.HasIndex(x => x.Status);
            });
        }
    }
}
