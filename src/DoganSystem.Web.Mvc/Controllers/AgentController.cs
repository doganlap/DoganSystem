using System;
using System.Threading.Tasks;
using DoganSystem.Modules.AgentOrchestrator.Application;
using DoganSystem.Modules.AgentOrchestrator.Application.Dtos;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    [Route("api/agents")]
    [ApiController]
    public class AgentController : AbpControllerBase
    {
        private readonly IEmployeeAgentAppService _agentAppService;

        public AgentController(IEmployeeAgentAppService agentAppService)
        {
            _agentAppService = agentAppService;
        }

        [HttpGet]
        public async Task<ActionResult<PagedResultDto<EmployeeAgentDto>>> GetList([FromQuery] EmployeeAgentListDto input)
        {
            return Ok(await _agentAppService.GetListAsync(input));
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<EmployeeAgentDto>> Get(Guid id)
        {
            return Ok(await _agentAppService.GetAsync(id));
        }

        [HttpPost]
        public async Task<ActionResult<EmployeeAgentDto>> Create([FromBody] CreateEmployeeAgentDto input)
        {
            return Ok(await _agentAppService.CreateAsync(input));
        }

        [HttpPut("{id}")]
        public async Task<ActionResult<EmployeeAgentDto>> Update(Guid id, [FromBody] UpdateEmployeeAgentDto input)
        {
            return Ok(await _agentAppService.UpdateAsync(id, input));
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult> Delete(Guid id)
        {
            await _agentAppService.DeleteAsync(id);
            return NoContent();
        }
    }
}
