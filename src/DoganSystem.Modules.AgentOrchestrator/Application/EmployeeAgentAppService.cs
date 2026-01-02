using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using DoganSystem.Modules.AgentOrchestrator.Application.Dtos;
using DoganSystem.Modules.AgentOrchestrator.Domain;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Configuration;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;

namespace DoganSystem.Modules.AgentOrchestrator.Application
{
    [Authorize]
    public class EmployeeAgentAppService : ApplicationService, IEmployeeAgentAppService
    {
        private readonly IRepository<EmployeeAgent, Guid> _agentRepository;
        private readonly IConfiguration _configuration;

        public EmployeeAgentAppService(
            IRepository<EmployeeAgent, Guid> agentRepository,
            IConfiguration configuration)
        {
            _agentRepository = agentRepository;
            _configuration = configuration;
        }

        public async Task<EmployeeAgentDto> CreateAsync(CreateEmployeeAgentDto input)
        {
            var agent = new EmployeeAgent
            {
                TenantId = input.TenantId,
                EmployeeName = input.EmployeeName,
                Role = input.Role,
                Department = input.Department,
                TeamId = input.TeamId,
                ManagerId = input.ManagerId,
                Status = "Available",
                Capabilities = input.Capabilities != null ? JsonSerializer.Serialize(input.Capabilities) : null,
                PythonServiceUrl = _configuration["PythonServices:OrchestratorUrl"]
            };

            agent = await _agentRepository.InsertAsync(agent);

            // Sync to Python orchestrator service (if configured)
            if (!string.IsNullOrEmpty(agent.PythonServiceUrl))
            {
                try
                {
                    var orchestratorService = LazyServiceProvider.LazyGetRequiredService<AgentOrchestratorService>();
                    await orchestratorService.SyncAgentToPythonServiceAsync(agent, agent.PythonServiceUrl);
                }
                catch
                {
                    // Python service may not be available, continue without sync
                }
            }

            return ObjectMapper.Map<EmployeeAgent, EmployeeAgentDto>(agent);
        }

        public async Task<EmployeeAgentDto> UpdateAsync(Guid id, UpdateEmployeeAgentDto input)
        {
            var agent = await _agentRepository.GetAsync(id);

            if (!string.IsNullOrEmpty(input.EmployeeName))
                agent.EmployeeName = input.EmployeeName;

            if (!string.IsNullOrEmpty(input.Role))
                agent.Role = input.Role;

            if (!string.IsNullOrEmpty(input.Department))
                agent.Department = input.Department;

            if (input.TeamId.HasValue)
                agent.TeamId = input.TeamId;

            if (input.ManagerId.HasValue)
                agent.ManagerId = input.ManagerId;

            if (!string.IsNullOrEmpty(input.Status))
                agent.Status = input.Status;

            if (input.Capabilities != null)
                agent.Capabilities = JsonSerializer.Serialize(input.Capabilities);

            agent = await _agentRepository.UpdateAsync(agent);

            // Sync to Python service (if configured)
            if (!string.IsNullOrEmpty(agent.PythonServiceUrl))
            {
                try
                {
                    var orchestratorService = LazyServiceProvider.LazyGetRequiredService<AgentOrchestratorService>();
                    await orchestratorService.SyncAgentToPythonServiceAsync(agent, agent.PythonServiceUrl);
                }
                catch
                {
                    // Python service may not be available, continue without sync
                }
            }

            return ObjectMapper.Map<EmployeeAgent, EmployeeAgentDto>(agent);
        }

        public async Task DeleteAsync(Guid id)
        {
            await _agentRepository.DeleteAsync(id);
        }

        public async Task<EmployeeAgentDto> GetAsync(Guid id)
        {
            var agent = await _agentRepository.GetAsync(id);
            var dto = ObjectMapper.Map<EmployeeAgent, EmployeeAgentDto>(agent);
            dto.Capabilities = JsonSerializer.Deserialize<List<string>>(agent.Capabilities ?? "[]") ?? new List<string>();
            return dto;
        }

        public async Task<PagedResultDto<EmployeeAgentDto>> GetListAsync(EmployeeAgentListDto input)
        {
            var queryable = await _agentRepository.GetQueryableAsync();

            if (input.TenantId.HasValue)
            {
                queryable = queryable.Where(x => x.TenantId == input.TenantId.Value);
            }

            if (!string.IsNullOrEmpty(input.Filter))
            {
                queryable = queryable.Where(x => 
                    x.EmployeeName.Contains(input.Filter) || 
                    x.Role.Contains(input.Filter));
            }

            if (!string.IsNullOrEmpty(input.Status))
            {
                queryable = queryable.Where(x => x.Status == input.Status);
            }

            if (!string.IsNullOrEmpty(input.Department))
            {
                queryable = queryable.Where(x => x.Department == input.Department);
            }

            if (!string.IsNullOrEmpty(input.Sorting))
            {
                // Simple sorting by property name
                if (input.Sorting.StartsWith("-"))
                {
                    var propName = input.Sorting.Substring(1).Trim();
                    if (propName.Equals("EmployeeName", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderByDescending(x => x.EmployeeName);
                    else if (propName.Equals("CreationTime", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderByDescending(x => x.CreationTime);
                    else
                        queryable = queryable.OrderByDescending(x => x.EmployeeName);
                }
                else
                {
                    var propName = input.Sorting.Trim();
                    if (propName.Equals("EmployeeName", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderBy(x => x.EmployeeName);
                    else if (propName.Equals("CreationTime", StringComparison.OrdinalIgnoreCase))
                        queryable = queryable.OrderBy(x => x.CreationTime);
                    else
                        queryable = queryable.OrderBy(x => x.EmployeeName);
                }
            }
            else
            {
                queryable = queryable.OrderBy(x => x.EmployeeName);
            }

            var totalCount = queryable.Count();
            var items = queryable
                .Skip(input.SkipCount)
                .Take(input.MaxResultCount)
                .ToList();

            var dtos = new List<EmployeeAgentDto>();
            foreach (var item in items)
            {
                var dto = ObjectMapper.Map<EmployeeAgent, EmployeeAgentDto>(item);
                dto.Capabilities = JsonSerializer.Deserialize<List<string>>(item.Capabilities ?? "[]") ?? new List<string>();
                dtos.Add(dto);
            }

            return new PagedResultDto<EmployeeAgentDto>(totalCount, dtos);
        }
    }

    public interface IEmployeeAgentAppService : IApplicationService
    {
        Task<EmployeeAgentDto> CreateAsync(CreateEmployeeAgentDto input);
        Task<EmployeeAgentDto> UpdateAsync(Guid id, UpdateEmployeeAgentDto input);
        Task DeleteAsync(Guid id);
        Task<EmployeeAgentDto> GetAsync(Guid id);
        Task<PagedResultDto<EmployeeAgentDto>> GetListAsync(EmployeeAgentListDto input);
    }
}
