using System;
using System.Threading.Tasks;
using DoganSystem.Modules.Subscription.Application;
using DoganSystem.Modules.Subscription.Application.Dtos;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class SubscriptionsMvcController : AbpController
    {
        private readonly ISubscriptionAppService _subscriptionAppService;

        public SubscriptionsMvcController(ISubscriptionAppService subscriptionAppService)
        {
            _subscriptionAppService = subscriptionAppService;
        }

        public async Task<IActionResult> Index()
        {
            var subscriptions = await _subscriptionAppService.GetListAsync(new SubscriptionListDto { MaxResultCount = 100 });
            return View(subscriptions.Items);
        }

        public async Task<IActionResult> Details(Guid id)
        {
            var subscription = await _subscriptionAppService.GetAsync(id);
            return View(subscription);
        }
    }
}
