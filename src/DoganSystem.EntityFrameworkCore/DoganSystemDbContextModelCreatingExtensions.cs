using Microsoft.EntityFrameworkCore;
using DoganSystem.Core.Domain.Entities;
using DoganSystem.Modules.ErpNext.Domain;
using DoganSystem.Modules.AgentOrchestrator.Domain;
using DoganSystem.Modules.Subscription.Domain;
using Volo.Abp.EntityFrameworkCore.Modeling;
using SubscriptionEntity = DoganSystem.Modules.Subscription.Domain.Subscription;

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
            
            // Note: Tenant entity is now managed by ABP TenantManagement module
            // The configuration is handled by builder.ConfigureTenantManagement() in DoganSystemDbContext
            
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
            builder.Entity<SubscriptionEntity>(b =>
            {
                b.ToTable("Subscriptions");
                b.ConfigureByConvention();
                b.Property(x => x.PlanType).IsRequired().HasMaxLength(50);
                b.Property(x => x.Status).IsRequired().HasMaxLength(50);
                b.Property(x => x.MonthlyPrice).HasPrecision(18, 2);
                b.HasIndex(x => x.TenantId);
                b.HasIndex(x => x.Status);
            });

            // Configure Contact Submissions (landing page contact form)
            builder.Entity<ContactSubmission>(b =>
            {
                b.ToTable("ContactSubmissions");
                b.ConfigureByConvention();
                b.Property(x => x.Name).IsRequired().HasMaxLength(100);
                b.Property(x => x.Email).IsRequired().HasMaxLength(200);
                b.Property(x => x.Company).HasMaxLength(200);
                b.Property(x => x.ServiceInterest).HasMaxLength(50);
                b.Property(x => x.Message).IsRequired().HasMaxLength(2000);
                b.Property(x => x.Status).HasMaxLength(50);
                b.Property(x => x.Notes).HasMaxLength(2000);
                b.Property(x => x.ErpNextLeadId).HasMaxLength(100);
                b.HasIndex(x => x.Email);
                b.HasIndex(x => x.Status);
                b.HasIndex(x => x.CreationTime);
            });
        }
    }
}
