using System;
using System.Threading.Tasks;
using DoganSystem.Modules.TenantManagement.Application;
using DoganSystem.Modules.TenantManagement.Application.Dtos;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Modules.TenantManagement.Web.Controllers
{
    [Route("api/tenants")]
    [ApiController]
    public class TenantController : AbpControllerBase
    {
        private readonly ITenantAppService _tenantAppService;

        public TenantController(ITenantAppService tenantAppService)
        {
            _tenantAppService = tenantAppService;
        }

        [HttpGet]
        public async Task<ActionResult<PagedResultDto<TenantDto>>> GetList([FromQuery] TenantListDto input)
        {
            return Ok(await _tenantAppService.GetListAsync(input));
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<TenantDto>> Get(Guid id)
        {
            return Ok(await _tenantAppService.GetAsync(id));
        }

        [HttpPost]
        public async Task<ActionResult<TenantDto>> Create([FromBody] CreateTenantDto input)
        {
            return Ok(await _tenantAppService.CreateAsync(input));
        }

        [HttpPut("{id}")]
        public async Task<ActionResult<TenantDto>> Update(Guid id, [FromBody] UpdateTenantDto input)
        {
            return Ok(await _tenantAppService.UpdateAsync(id, input));
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult> Delete(Guid id)
        {
            await _tenantAppService.DeleteAsync(id);
            return NoContent();
        }

        [HttpPost("{id}/activate")]
        public async Task<ActionResult<TenantDto>> Activate(Guid id)
        {
            return Ok(await _tenantAppService.ActivateAsync(id));
        }

        [HttpPost("{id}/suspend")]
        public async Task<ActionResult<TenantDto>> Suspend(Guid id)
        {
            return Ok(await _tenantAppService.SuspendAsync(id));
        }
    }
}
