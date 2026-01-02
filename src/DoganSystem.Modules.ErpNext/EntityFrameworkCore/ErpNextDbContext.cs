using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.ErpNext.Domain;
using Volo.Abp.Data;
using Volo.Abp.EntityFrameworkCore;

namespace DoganSystem.Modules.ErpNext.EntityFrameworkCore
{
    [ConnectionStringName("Default")]
    public class ErpNextDbContext : AbpDbContext<ErpNextDbContext>
    {
        public DbSet<ErpNextInstance> ErpNextInstances { get; set; }

        public ErpNextDbContext(DbContextOptions<ErpNextDbContext> options)
            : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);
            builder.ConfigureErpNext();
        }
    }
}
