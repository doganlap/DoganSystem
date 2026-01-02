using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.ErpNext.Domain;
using Volo.Abp.EntityFrameworkCore.Modeling;

namespace DoganSystem.Modules.ErpNext.EntityFrameworkCore
{
    public static class ErpNextDbContextModelCreatingExtensions
    {
        public static void ConfigureErpNext(this ModelBuilder builder)
        {
            builder.Entity<ErpNextInstance>(b =>
            {
                b.ToTable("ErpNextInstances");
                b.ConfigureByConvention();
                b.Property(x => x.Name).IsRequired().HasMaxLength(256);
                b.Property(x => x.BaseUrl).IsRequired().HasMaxLength(512);
                b.HasIndex(x => x.TenantId);
            });
        }
    }
}
