using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DoganSystem.Modules.TenantManagement.Application.Dtos;
using DoganSystem.Modules.TenantManagement.Domain;
using Microsoft.AspNetCore.Authorization;
using Volo.Abp;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;

namespace DoganSystem.Modules.TenantManagement.Application
{
    [Authorize]
    public class TenantAppService : ApplicationService, ITenantAppService
    {
        private readonly IRepository<Tenant, Guid> _tenantRepository;

        public TenantAppService(IRepository<Tenant, Guid> tenantRepository)
        {
            _tenantRepository = tenantRepository;
        }

        public async Task<TenantDto> CreateAsync(CreateTenantDto input)
        {
            // Check if subdomain already exists
            if (!string.IsNullOrEmpty(input.Subdomain))
            {
                var existing = await _tenantRepository.FirstOrDefaultAsync(x => x.Subdomain == input.Subdomain);
                if (existing != null)
                {
                    throw new UserFriendlyException($"Subdomain '{input.Subdomain}' is already taken.");
                }
            }

            var tenant = new Tenant
            {
                Name = input.Name,
                Subdomain = input.Subdomain,
                Domain = input.Domain,
                SubscriptionTier = input.SubscriptionTier,
                Status = "Trial",
                TrialEndDate = DateTime.UtcNow.AddDays(input.TrialDays),
                Metadata = input.Metadata
            };

            tenant = await _tenantRepository.InsertAsync(tenant);

            return ObjectMapper.Map<Tenant, TenantDto>(tenant);
        }

        public async Task<TenantDto> UpdateAsync(Guid id, UpdateTenantDto input)
        {
            var tenant = await _tenantRepository.GetAsync(id);

            if (!string.IsNullOrEmpty(input.Name))
                tenant.Name = input.Name;

            if (!string.IsNullOrEmpty(input.Domain))
                tenant.Domain = input.Domain;

            if (!string.IsNullOrEmpty(input.Status))
                tenant.Status = input.Status;

            if (!string.IsNullOrEmpty(input.SubscriptionTier))
                tenant.SubscriptionTier = input.SubscriptionTier;

            if (input.Metadata != null)
                tenant.Metadata = input.Metadata;

            tenant = await _tenantRepository.UpdateAsync(tenant);

            return ObjectMapper.Map<Tenant, TenantDto>(tenant);
        }

        public async Task DeleteAsync(Guid id)
        {
            await _tenantRepository.DeleteAsync(id);
        }

        public async Task<TenantDto> GetAsync(Guid id)
        {
            var tenant = await _tenantRepository.GetAsync(id);
            return ObjectMapper.Map<Tenant, TenantDto>(tenant);
        }

        public async Task<PagedResultDto<TenantDto>> GetListAsync(TenantListDto input)
        {
            var queryable = await _tenantRepository.GetQueryableAsync();

            // Apply filters
            if (!string.IsNullOrEmpty(input.Filter))
            {
                queryable = queryable.Where(x => 
                    x.Name.Contains(input.Filter) || 
                    x.Subdomain.Contains(input.Filter) ||
                    x.Domain.Contains(input.Filter));
            }

            if (!string.IsNullOrEmpty(input.Status))
            {
                queryable = queryable.Where(x => x.Status == input.Status);
            }

            if (!string.IsNullOrEmpty(input.SubscriptionTier))
            {
                queryable = queryable.Where(x => x.SubscriptionTier == input.SubscriptionTier);
            }

            // Apply sorting
            if (!string.IsNullOrEmpty(input.Sorting))
            {
                // Simple sorting by property name
                if (input.Sorting.StartsWith("-"))
                {
                    var propName = input.Sorting.Substring(1).Trim();
                    if (propName.Equals("Name", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderByDescending(x => x.Name);
                    else if (propName.Equals("CreationTime", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderByDescending(x => x.CreationTime);
                    else
                        queryable = queryable.OrderByDescending(x => x.CreationTime);
                }
                else
                {
                    var propName = input.Sorting.Trim();
                    if (propName.Equals("Name", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderBy(x => x.Name);
                    else if (propName.Equals("CreationTime", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderBy(x => x.CreationTime);
                    else
                        queryable = queryable.OrderBy(x => x.CreationTime);
                }
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

            return new PagedResultDto<TenantDto>(
                totalCount,
                ObjectMapper.Map<List<Tenant>, List<TenantDto>>(items)
            );
        }

        public async Task<TenantDto> ActivateAsync(Guid id)
        {
            var tenant = await _tenantRepository.GetAsync(id);
            tenant.Status = "Active";
            tenant = await _tenantRepository.UpdateAsync(tenant);
            return ObjectMapper.Map<Tenant, TenantDto>(tenant);
        }

        public async Task<TenantDto> SuspendAsync(Guid id)
        {
            var tenant = await _tenantRepository.GetAsync(id);
            tenant.Status = "Suspended";
            tenant = await _tenantRepository.UpdateAsync(tenant);
            return ObjectMapper.Map<Tenant, TenantDto>(tenant);
        }
    }

    public interface ITenantAppService : IApplicationService
    {
        Task<TenantDto> CreateAsync(CreateTenantDto input);
        Task<TenantDto> UpdateAsync(Guid id, UpdateTenantDto input);
        Task DeleteAsync(Guid id);
        Task<TenantDto> GetAsync(Guid id);
        Task<PagedResultDto<TenantDto>> GetListAsync(TenantListDto input);
        Task<TenantDto> ActivateAsync(Guid id);
        Task<TenantDto> SuspendAsync(Guid id);
    }
}
