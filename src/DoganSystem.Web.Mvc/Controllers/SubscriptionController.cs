using System;
using System.Threading.Tasks;
using DoganSystem.Modules.Subscription.Application;
using DoganSystem.Modules.Subscription.Application.Dtos;
using DoganSystem.Permissions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.Application.Dtos;

namespace DoganSystem.Web.Mvc.Controllers
{
    [Route("api/subscriptions")]
    [ApiController]
    public class SubscriptionController : AbpControllerBase
    {
        private readonly ISubscriptionAppService _subscriptionAppService;

        public SubscriptionController(ISubscriptionAppService subscriptionAppService)
        {
            _subscriptionAppService = subscriptionAppService;
        }

        [HttpGet]
        [Authorize(GrcPermissions.Subscriptions.View)]
        public async Task<ActionResult<PagedResultDto<SubscriptionDto>>> GetList([FromQuery] SubscriptionListDto input)
        {
            return Ok(await _subscriptionAppService.GetListAsync(input));
        }

        [HttpGet("{id}")]
        [Authorize(GrcPermissions.Subscriptions.View)]
        public async Task<ActionResult<SubscriptionDto>> Get(Guid id)
        {
            return Ok(await _subscriptionAppService.GetAsync(id));
        }

        [HttpGet("tenant/{tenantId}")]
        [Authorize(GrcPermissions.Subscriptions.View)]
        public async Task<ActionResult<SubscriptionDto>> GetByTenant(Guid tenantId)
        {
            return Ok(await _subscriptionAppService.GetByTenantIdAsync(tenantId));
        }

        [HttpPost]
        [Authorize(GrcPermissions.Subscriptions.Manage)]
        public async Task<ActionResult<SubscriptionDto>> Create([FromBody] CreateSubscriptionDto input)
        {
            return Ok(await _subscriptionAppService.CreateAsync(input));
        }

        [HttpPut("{id}")]
        [Authorize(GrcPermissions.Subscriptions.Manage)]
        public async Task<ActionResult<SubscriptionDto>> Update(Guid id, [FromBody] UpdateSubscriptionDto input)
        {
            return Ok(await _subscriptionAppService.UpdateAsync(id, input));
        }

        [HttpDelete("{id}")]
        [Authorize(GrcPermissions.Subscriptions.Manage)]
        public async Task<ActionResult> Delete(Guid id)
        {
            await _subscriptionAppService.DeleteAsync(id);
            return NoContent();
        }

        [HttpPost("{id}/cancel")]
        [Authorize(GrcPermissions.Subscriptions.Manage)]
        public async Task<ActionResult<SubscriptionDto>> Cancel(Guid id)
        {
            return Ok(await _subscriptionAppService.CancelAsync(id));
        }

        [HttpPost("{id}/renew")]
        [Authorize(GrcPermissions.Subscriptions.Manage)]
        public async Task<ActionResult<SubscriptionDto>> Renew(Guid id)
        {
            return Ok(await _subscriptionAppService.RenewAsync(id));
        }
    }
}
