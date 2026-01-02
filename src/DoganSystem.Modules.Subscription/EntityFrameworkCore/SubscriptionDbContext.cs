using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.Subscription.Domain;
using Volo.Abp.Data;
using Volo.Abp.EntityFrameworkCore;
using SubscriptionEntity = DoganSystem.Modules.Subscription.Domain.Subscription;

namespace DoganSystem.Modules.Subscription.EntityFrameworkCore
{
    [ConnectionStringName("Default")]
    public class SubscriptionDbContext : AbpDbContext<SubscriptionDbContext>
    {
        public DbSet<SubscriptionEntity> Subscriptions { get; set; }

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
