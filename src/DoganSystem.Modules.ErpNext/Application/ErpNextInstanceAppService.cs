using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
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
        private readonly IHttpClientFactory _httpClientFactory;

        public ErpNextInstanceAppService(
            IRepository<ErpNextInstance, Guid> erpNextRepository,
            IHttpClientFactory httpClientFactory)
        {
            _erpNextRepository = erpNextRepository;
            _httpClientFactory = httpClientFactory;
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

            return new PagedResultDto<ErpNextInstanceDto>(
                totalCount,
                ObjectMapper.Map<List<ErpNextInstance>, List<ErpNextInstanceDto>>(items)
            );
        }

        public async Task<ErpNextInstanceDto> TestConnectionAsync(Guid id)
        {
            var instance = await _erpNextRepository.GetAsync(id);

            // Test ERPNext connection using IHttpClientFactory (built-in .NET best practice)
            try
            {
                var client = _httpClientFactory.CreateClient("ErpNext");
                client.Timeout = TimeSpan.FromSeconds(30);

                // Build ERPNext API URL
                var apiUrl = $"{instance.BaseUrl.TrimEnd('/')}/api/resource/User";

                // Create request with authentication headers if API key is provided
                var request = new HttpRequestMessage(HttpMethod.Get, apiUrl);
                if (!string.IsNullOrEmpty(instance.ApiKey) && !string.IsNullOrEmpty(instance.ApiSecret))
                {
                    request.Headers.Add("Authorization", $"token {instance.ApiKey}:{instance.ApiSecret}");
                }

                // Test connection with a simple GET request
                var response = await client.SendAsync(request);

                if (!response.IsSuccessStatusCode)
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    throw new UserFriendlyException($"ERPNext API returned status {response.StatusCode}: {errorContent}");
                }

                instance.LastSyncTime = DateTime.UtcNow;
                instance = await _erpNextRepository.UpdateAsync(instance);

                return ObjectMapper.Map<ErpNextInstance, ErpNextInstanceDto>(instance);
            }
            catch (HttpRequestException ex)
            {
                throw new UserFriendlyException($"Failed to connect to ERPNext at {instance.BaseUrl}: {ex.Message}");
            }
            catch (TaskCanceledException)
            {
                throw new UserFriendlyException($"Connection to ERPNext timed out after 30 seconds");
            }
            catch (UserFriendlyException)
            {
                throw;
            }
            catch (Exception ex)
            {
                throw new UserFriendlyException($"Failed to test ERPNext connection: {ex.Message}");
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
