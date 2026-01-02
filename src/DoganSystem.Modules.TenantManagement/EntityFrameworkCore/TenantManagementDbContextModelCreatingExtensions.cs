using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.TenantManagement.Domain;
using Volo.Abp.EntityFrameworkCore.Modeling;

namespace DoganSystem.Modules.TenantManagement.EntityFrameworkCore
{
    public static class TenantManagementDbContextModelCreatingExtensions
    {
        public static void ConfigureTenantManagement(this ModelBuilder builder)
        {
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
        }
    }
}
