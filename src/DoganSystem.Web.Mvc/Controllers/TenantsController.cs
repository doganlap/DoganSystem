using System;
using System.Threading.Tasks;
using DoganSystem.Modules.TenantManagement.Application;
using DoganSystem.Modules.TenantManagement.Application.Dtos;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class TenantsController : AbpController
    {
        private readonly ITenantAppService _tenantAppService;

        public TenantsController(ITenantAppService tenantAppService)
        {
            _tenantAppService = tenantAppService;
        }

        public async Task<IActionResult> Index()
        {
            var tenants = await _tenantAppService.GetListAsync(new TenantListDto { MaxResultCount = 100 });
            return View(tenants.Items);
        }

        public async Task<IActionResult> Details(Guid id)
        {
            var tenant = await _tenantAppService.GetAsync(id);
            return View(tenant);
        }

        public IActionResult Create()
        {
            return View(new CreateTenantDto());
        }

        [HttpPost]
        public async Task<IActionResult> Create(CreateTenantDto input)
        {
            if (ModelState.IsValid)
            {
                await _tenantAppService.CreateAsync(input);
                return RedirectToAction("Index");
            }
            return View(input);
        }

        public async Task<IActionResult> Edit(Guid id)
        {
            var tenant = await _tenantAppService.GetAsync(id);
            var updateDto = new UpdateTenantDto
            {
                Name = tenant.Name,
                Domain = tenant.Domain,
                Status = tenant.Status,
                SubscriptionTier = tenant.SubscriptionTier
            };
            return View(updateDto);
        }

        [HttpPost]
        public async Task<IActionResult> Edit(Guid id, UpdateTenantDto input)
        {
            if (ModelState.IsValid)
            {
                await _tenantAppService.UpdateAsync(id, input);
                return RedirectToAction("Index");
            }
            return View(input);
        }
    }
}
