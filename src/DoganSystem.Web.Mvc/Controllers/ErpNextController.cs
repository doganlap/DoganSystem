using System;
using System.Threading.Tasks;
using DoganSystem.Modules.ErpNext.Application;
using DoganSystem.Modules.ErpNext.Application.Dtos;
using DoganSystem.Permissions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.Application.Dtos;

namespace DoganSystem.Web.Mvc.Controllers
{
    [Route("api/erpnext")]
    [ApiController]
    public class ErpNextController : AbpControllerBase
    {
        private readonly IErpNextInstanceAppService _erpNextAppService;

        public ErpNextController(IErpNextInstanceAppService erpNextAppService)
        {
            _erpNextAppService = erpNextAppService;
        }

        [HttpGet]
        [Authorize(GrcPermissions.Integrations.View)]
        public async Task<ActionResult<PagedResultDto<ErpNextInstanceDto>>> GetList([FromQuery] ErpNextInstanceListDto input)
        {
            return Ok(await _erpNextAppService.GetListAsync(input));
        }

        [HttpGet("{id}")]
        [Authorize(GrcPermissions.Integrations.View)]
        public async Task<ActionResult<ErpNextInstanceDto>> Get(Guid id)
        {
            return Ok(await _erpNextAppService.GetAsync(id));
        }

        [HttpPost]
        [Authorize(GrcPermissions.Integrations.Manage)]
        public async Task<ActionResult<ErpNextInstanceDto>> Create([FromBody] CreateErpNextInstanceDto input)
        {
            return Ok(await _erpNextAppService.CreateAsync(input));
        }

        [HttpPut("{id}")]
        [Authorize(GrcPermissions.Integrations.Manage)]
        public async Task<ActionResult<ErpNextInstanceDto>> Update(Guid id, [FromBody] UpdateErpNextInstanceDto input)
        {
            return Ok(await _erpNextAppService.UpdateAsync(id, input));
        }

        [HttpDelete("{id}")]
        [Authorize(GrcPermissions.Integrations.Manage)]
        public async Task<ActionResult> Delete(Guid id)
        {
            await _erpNextAppService.DeleteAsync(id);
            return NoContent();
        }

        [HttpPost("{id}/test-connection")]
        [Authorize(GrcPermissions.Integrations.Manage)]
        public async Task<ActionResult<ErpNextInstanceDto>> TestConnection(Guid id)
        {
            return Ok(await _erpNextAppService.TestConnectionAsync(id));
        }
    }
}
