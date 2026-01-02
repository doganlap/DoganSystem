using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DoganSystem.Modules.Subscription.Application.Dtos;
using DoganSystem.Modules.Subscription.Domain;
using Microsoft.AspNetCore.Authorization;
using Volo.Abp;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;

namespace DoganSystem.Modules.Subscription.Application
{
    [Authorize]
    public class SubscriptionAppService : ApplicationService, ISubscriptionAppService
    {
        private readonly IRepository<Subscription, Guid> _subscriptionRepository;

        // Plan pricing
        private readonly Dictionary<string, decimal> _planPricing = new()
        {
            { "Starter", 99.00m },
            { "Professional", 299.00m },
            { "Enterprise", 999.00m }
        };

        public SubscriptionAppService(IRepository<Subscription, Guid> subscriptionRepository)
        {
            _subscriptionRepository = subscriptionRepository;
        }

        public async Task<SubscriptionDto> CreateAsync(CreateSubscriptionDto input)
        {
            var subscription = new Subscription
            {
                TenantId = input.TenantId,
                PlanType = input.PlanType,
                StartDate = input.StartDate ?? DateTime.UtcNow,
                EndDate = input.EndDate,
                Status = "Active",
                MonthlyPrice = _planPricing.GetValueOrDefault(input.PlanType, 0),
                PaymentProvider = input.PaymentProvider,
                PaymentProviderSubscriptionId = input.PaymentProviderSubscriptionId,
                NextBillingDate = (input.StartDate ?? DateTime.UtcNow).AddMonths(1)
            };

            subscription = await _subscriptionRepository.InsertAsync(subscription);

            return ObjectMapper.Map<Subscription, SubscriptionDto>(subscription);
        }

        public async Task<SubscriptionDto> UpdateAsync(Guid id, UpdateSubscriptionDto input)
        {
            var subscription = await _subscriptionRepository.GetAsync(id);

            if (!string.IsNullOrEmpty(input.PlanType))
            {
                subscription.PlanType = input.PlanType;
                subscription.MonthlyPrice = _planPricing.GetValueOrDefault(input.PlanType, subscription.MonthlyPrice);
            }

            if (!string.IsNullOrEmpty(input.Status))
                subscription.Status = input.Status;

            if (input.EndDate.HasValue)
                subscription.EndDate = input.EndDate;

            if (input.MonthlyPrice.HasValue)
                subscription.MonthlyPrice = input.MonthlyPrice.Value;

            subscription = await _subscriptionRepository.UpdateAsync(subscription);

            return ObjectMapper.Map<Subscription, SubscriptionDto>(subscription);
        }

        public async Task DeleteAsync(Guid id)
        {
            await _subscriptionRepository.DeleteAsync(id);
        }

        public async Task<SubscriptionDto> GetAsync(Guid id)
        {
            var subscription = await _subscriptionRepository.GetAsync(id);
            return ObjectMapper.Map<Subscription, SubscriptionDto>(subscription);
        }

        public async Task<SubscriptionDto> GetByTenantIdAsync(Guid tenantId)
        {
            var subscription = await _subscriptionRepository.FirstOrDefaultAsync(x => x.TenantId == tenantId && x.Status == "Active");
            if (subscription == null)
                throw new UserFriendlyException($"No active subscription found for tenant {tenantId}");

            return ObjectMapper.Map<Subscription, SubscriptionDto>(subscription);
        }

        public async Task<PagedResultDto<SubscriptionDto>> GetListAsync(SubscriptionListDto input)
        {
            var queryable = await _subscriptionRepository.GetQueryableAsync();

            if (input.TenantId.HasValue)
            {
                queryable = queryable.Where(x => x.TenantId == input.TenantId.Value);
            }

            if (!string.IsNullOrEmpty(input.Status))
            {
                queryable = queryable.Where(x => x.Status == input.Status);
            }

            if (!string.IsNullOrEmpty(input.PlanType))
            {
                queryable = queryable.Where(x => x.PlanType == input.PlanType);
            }

            if (!string.IsNullOrEmpty(input.Sorting))
            {
                queryable = queryable.OrderBy(input.Sorting);
            }
            else
            {
                queryable = queryable.OrderByDescending(x => x.CreationTime);
            }

            var totalCount = queryable.Count();
            var items = queryable
                .Skip(input.SkipCount)
                .Take(input.MaxResultCount)
                .ToList();

            return new PagedResultDto<SubscriptionDto>(
                totalCount,
                ObjectMapper.Map<List<Subscription>, List<SubscriptionDto>>(items)
            );
        }

        public async Task<SubscriptionDto> CancelAsync(Guid id)
        {
            var subscription = await _subscriptionRepository.GetAsync(id);
            subscription.Status = "Cancelled";
            subscription.EndDate = DateTime.UtcNow;
            subscription = await _subscriptionRepository.UpdateAsync(subscription);
            return ObjectMapper.Map<Subscription, SubscriptionDto>(subscription);
        }

        public async Task<SubscriptionDto> RenewAsync(Guid id)
        {
            var subscription = await _subscriptionRepository.GetAsync(id);
            subscription.Status = "Active";
            subscription.NextBillingDate = DateTime.UtcNow.AddMonths(1);
            subscription = await _subscriptionRepository.UpdateAsync(subscription);
            return ObjectMapper.Map<Subscription, SubscriptionDto>(subscription);
        }
    }

    public interface ISubscriptionAppService : IApplicationService
    {
        Task<SubscriptionDto> CreateAsync(CreateSubscriptionDto input);
        Task<SubscriptionDto> UpdateAsync(Guid id, UpdateSubscriptionDto input);
        Task DeleteAsync(Guid id);
        Task<SubscriptionDto> GetAsync(Guid id);
        Task<SubscriptionDto> GetByTenantIdAsync(Guid tenantId);
        Task<PagedResultDto<SubscriptionDto>> GetListAsync(SubscriptionListDto input);
        Task<SubscriptionDto> CancelAsync(Guid id);
        Task<SubscriptionDto> RenewAsync(Guid id);
    }
}
