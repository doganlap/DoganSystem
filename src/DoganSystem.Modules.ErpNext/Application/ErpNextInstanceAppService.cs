using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DoganSystem.Modules.ErpNext.Application.Dtos;
using DoganSystem.Modules.ErpNext.Domain;
using Microsoft.AspNetCore.Authorization;
using Volo.Abp;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;

namespace DoganSystem.Modules.ErpNext.Application
{
    [Authorize]
    public class ErpNextInstanceAppService : ApplicationService, IErpNextInstanceAppService
    {
        private readonly IRepository<ErpNextInstance, Guid> _erpNextRepository;

        public ErpNextInstanceAppService(IRepository<ErpNextInstance, Guid> erpNextRepository)
        {
            _erpNextRepository = erpNextRepository;
        }

        public async Task<ErpNextInstanceDto> CreateAsync(CreateErpNextInstanceDto input)
        {
            var instance = new ErpNextInstance
            {
                Name = input.Name,
                BaseUrl = input.BaseUrl,
                ApiKey = input.ApiKey,
                ApiSecret = input.ApiSecret,
                SiteName = input.SiteName,
                TenantId = input.TenantId,
                Description = input.Description,
                IsActive = true
            };

            instance = await _erpNextRepository.InsertAsync(instance);

            return ObjectMapper.Map<ErpNextInstance, ErpNextInstanceDto>(instance);
        }

        public async Task<ErpNextInstanceDto> UpdateAsync(Guid id, UpdateErpNextInstanceDto input)
        {
            var instance = await _erpNextRepository.GetAsync(id);

            if (!string.IsNullOrEmpty(input.Name))
                instance.Name = input.Name;

            if (!string.IsNullOrEmpty(input.BaseUrl))
                instance.BaseUrl = input.BaseUrl;

            if (!string.IsNullOrEmpty(input.ApiKey))
                instance.ApiKey = input.ApiKey;

            if (!string.IsNullOrEmpty(input.ApiSecret))
                instance.ApiSecret = input.ApiSecret;

            if (!string.IsNullOrEmpty(input.SiteName))
                instance.SiteName = input.SiteName;

            if (input.IsActive.HasValue)
                instance.IsActive = input.IsActive.Value;

            if (input.Description != null)
                instance.Description = input.Description;

            instance = await _erpNextRepository.UpdateAsync(instance);

            return ObjectMapper.Map<ErpNextInstance, ErpNextInstanceDto>(instance);
        }

        public async Task DeleteAsync(Guid id)
        {
            await _erpNextRepository.DeleteAsync(id);
        }

        public async Task<ErpNextInstanceDto> GetAsync(Guid id)
        {
            var instance = await _erpNextRepository.GetAsync(id);
            return ObjectMapper.Map<ErpNextInstance, ErpNextInstanceDto>(instance);
        }

        public async Task<PagedResultDto<ErpNextInstanceDto>> GetListAsync(ErpNextInstanceListDto input)
        {
            var queryable = await _erpNextRepository.GetQueryableAsync();

            if (!string.IsNullOrEmpty(input.Filter))
            {
                queryable = queryable.Where(x => 
                    x.Name.Contains(input.Filter) || 
                    x.BaseUrl.Contains(input.Filter));
            }

            if (input.TenantId.HasValue)
            {
                queryable = queryable.Where(x => x.TenantId == input.TenantId.Value);
            }

            if (input.IsActive.HasValue)
            {
                queryable = queryable.Where(x => x.IsActive == input.IsActive.Value);
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

            return new PagedResultDto<ErpNextInstanceDto>(
                totalCount,
                ObjectMapper.Map<List<ErpNextInstance>, List<ErpNextInstanceDto>>(items)
            );
        }

        public async Task<ErpNextInstanceDto> TestConnectionAsync(Guid id)
        {
            var instance = await _erpNextRepository.GetAsync(id);
            
            // Test ERPNext connection
            try
            {
                // TODO: Implement actual ERPNext API test
                // var client = new HttpClient();
                // var response = await client.GetAsync($"{instance.BaseUrl}/api/resource/User");
                // response.EnsureSuccessStatusCode();
                
                instance.LastSyncTime = DateTime.UtcNow;
                instance = await _erpNextRepository.UpdateAsync(instance);
                
                return ObjectMapper.Map<ErpNextInstance, ErpNextInstanceDto>(instance);
            }
            catch (Exception ex)
            {
                throw new UserFriendlyException($"Failed to connect to ERPNext: {ex.Message}");
            }
        }
    }

    public interface IErpNextInstanceAppService : IApplicationService
    {
        Task<ErpNextInstanceDto> CreateAsync(CreateErpNextInstanceDto input);
        Task<ErpNextInstanceDto> UpdateAsync(Guid id, UpdateErpNextInstanceDto input);
        Task DeleteAsync(Guid id);
        Task<ErpNextInstanceDto> GetAsync(Guid id);
        Task<PagedResultDto<ErpNextInstanceDto>> GetListAsync(ErpNextInstanceListDto input);
        Task<ErpNextInstanceDto> TestConnectionAsync(Guid id);
    }
}
