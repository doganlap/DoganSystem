using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.Subscription.Domain;
using Volo.Abp.Data;
using Volo.Abp.EntityFrameworkCore;

namespace DoganSystem.Modules.Subscription.EntityFrameworkCore
{
    [ConnectionStringName("Default")]
    public class SubscriptionDbContext : AbpDbContext<SubscriptionDbContext>
    {
        public DbSet<Subscription> Subscriptions { get; set; }

        public SubscriptionDbContext(DbContextOptions<SubscriptionDbContext> options)
            : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);
            builder.ConfigureSubscription();
        }
    }
}
