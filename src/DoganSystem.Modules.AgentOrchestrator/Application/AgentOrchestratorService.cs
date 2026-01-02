using DoganSystem.Modules.AgentOrchestrator.Domain;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RestSharp;
using System.Text.Json;
using Volo.Abp.Domain.Repositories;
using Volo.Abp.Domain.Services;

namespace DoganSystem.Modules.AgentOrchestrator.Application
{
    public class AgentOrchestratorService : DomainService
    {
        private readonly IRepository<EmployeeAgent, Guid> _agentRepository;
        private readonly IConfiguration _configuration;

        private readonly ILogger<AgentOrchestratorService> _logger;

        public AgentOrchestratorService(
            IRepository<EmployeeAgent, Guid> agentRepository,
            IConfiguration configuration,
            ILogger<AgentOrchestratorService> logger)
        {
            _agentRepository = agentRepository;
            _configuration = configuration;
            _logger = logger;
        }

        public async Task<EmployeeAgent> CreateAgentAsync(EmployeeAgent agent)
        {
            // Save to database
            await _agentRepository.InsertAsync(agent);

            // Call Python orchestrator service
            var pythonServiceUrl = _configuration["PythonServices:OrchestratorUrl"] ?? "http://localhost:8006";
            await SyncAgentToPythonServiceAsync(agent, pythonServiceUrl);

            return agent;
        }

        public async Task SyncAgentToPythonServiceAsync(EmployeeAgent agent, string pythonServiceUrl)
        {
            try
            {
                var client = new RestClient(pythonServiceUrl);
                var request = new RestRequest($"/api/v1/{agent.TenantId}/agents", Method.Post);
                request.AddJsonBody(new
                {
                    employee_name = agent.EmployeeName,
                    role = agent.Role,
                    department = agent.Department,
                    capabilities = JsonSerializer.Deserialize<string[]>(agent.Capabilities ?? "[]")
                });

                var response = await client.ExecuteAsync(request);
                if (!response.IsSuccessful)
                {
                    // Log error
                    _logger.LogWarning("Failed to sync agent {AgentId} to Python service: {ErrorMessage}", agent.Id, response.ErrorMessage);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error syncing agent {AgentId} to Python service", agent.Id);
            }
        }

        public async Task<List<EmployeeAgent>> GetAgentsByTenantAsync(Guid tenantId)
        {
            return await _agentRepository.GetListAsync(x => x.TenantId == tenantId);
        }
    }
}
