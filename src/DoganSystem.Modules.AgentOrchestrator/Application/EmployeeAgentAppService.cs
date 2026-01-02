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
        private readonly AgentOrchestratorService _orchestratorService;
        private readonly IConfiguration _configuration;

        public EmployeeAgentAppService(
            IRepository<EmployeeAgent, Guid> agentRepository,
            AgentOrchestratorService orchestratorService,
            IConfiguration configuration)
        {
            _agentRepository = agentRepository;
            _orchestratorService = orchestratorService;
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
                Capabilities = JsonSerializer.Serialize(input.Capabilities ?? new List<string>()),
                PythonServiceUrl = _configuration["PythonServices:OrchestratorUrl"] ?? "http://localhost:8006"
            };

            agent = await _agentRepository.InsertAsync(agent);

            // Sync to Python orchestrator service
            await _orchestratorService.SyncAgentToPythonServiceAsync(agent, agent.PythonServiceUrl);

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

            // Sync to Python service
            await _orchestratorService.SyncAgentToPythonServiceAsync(agent, agent.PythonServiceUrl);

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
            dto.Capabilities = JsonSerializer.Deserialize<List<string>>(agent.Capabilities ?? "[]");
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
                queryable = queryable.OrderBy(input.Sorting);
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
                dto.Capabilities = JsonSerializer.Deserialize<List<string>>(item.Capabilities ?? "[]");
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
