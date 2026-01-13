using System;
using System.Threading.Tasks;
using DoganSystem.Modules.AgentOrchestrator.Application;
using DoganSystem.Modules.AgentOrchestrator.Application.Dtos;
using DoganSystem.Permissions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    [Authorize(GrcPermissions.Admin.Access)]
    public class AgentsController : AbpController
    {
        private readonly IEmployeeAgentAppService _agentAppService;

        public AgentsController(IEmployeeAgentAppService agentAppService)
        {
            _agentAppService = agentAppService;
        }

        public async Task<IActionResult> Index()
        {
            var agents = await _agentAppService.GetListAsync(new EmployeeAgentListDto { MaxResultCount = 100 });
            return View(agents.Items);
        }

        public async Task<IActionResult> Details(Guid id)
        {
            var agent = await _agentAppService.GetAsync(id);
            return View(agent);
        }

        public IActionResult Create()
        {
            return View(new CreateEmployeeAgentDto
            {
                EmployeeName = string.Empty,
                Role = string.Empty
            });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(CreateEmployeeAgentDto input)
        {
            if (ModelState.IsValid)
            {
                await _agentAppService.CreateAsync(input);
                return RedirectToAction("Index");
            }
            return View(input);
        }

        public async Task<IActionResult> Edit(Guid id)
        {
            var agent = await _agentAppService.GetAsync(id);
            var updateDto = new UpdateEmployeeAgentDto
            {
                EmployeeName = agent.EmployeeName,
                Role = agent.Role,
                Department = agent.Department,
                Status = agent.Status,
                Capabilities = agent.Capabilities
            };
            return View(updateDto);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(Guid id, UpdateEmployeeAgentDto input)
        {
            if (ModelState.IsValid)
            {
                await _agentAppService.UpdateAsync(id, input);
                return RedirectToAction("Index");
            }
            return View(input);
        }
    }
}
