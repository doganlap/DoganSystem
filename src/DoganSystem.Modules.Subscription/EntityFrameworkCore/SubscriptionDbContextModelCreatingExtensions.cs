using Microsoft.EntityFrameworkCore;
using DoganSystem.Modules.Subscription.Domain;
using Volo.Abp.EntityFrameworkCore.Modeling;
using SubscriptionEntity = DoganSystem.Modules.Subscription.Domain.Subscription;

namespace DoganSystem.Modules.Subscription.EntityFrameworkCore
{
    public static class SubscriptionDbContextModelCreatingExtensions
    {
        public static void ConfigureSubscription(this ModelBuilder builder)
        {
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
        }
    }
}
