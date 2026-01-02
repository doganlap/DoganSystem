using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.TenantManagement.Domain;
using Volo.Abp.Data;
using Volo.Abp.EntityFrameworkCore;

namespace DoganSystem.Modules.TenantManagement.EntityFrameworkCore
{
    [ConnectionStringName("Default")]
    public class TenantManagementDbContext : AbpDbContext<TenantManagementDbContext>
    {
        public DbSet<Tenant> Tenants { get; set; }

        public TenantManagementDbContext(DbContextOptions<TenantManagementDbContext> options)
            : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);
            builder.ConfigureTenantManagement();
        }
    }
}
