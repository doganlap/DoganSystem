using System;
using System.Threading.Tasks;
using DoganSystem.Modules.ErpNext.Application;
using DoganSystem.Modules.ErpNext.Application.Dtos;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class ErpNextMvcController : AbpController
    {
        private readonly IErpNextInstanceAppService _erpNextAppService;

        public ErpNextMvcController(IErpNextInstanceAppService erpNextAppService)
        {
            _erpNextAppService = erpNextAppService;
        }

        // GET: /ErpNext
        public async Task<IActionResult> Index()
        {
            var instances = await _erpNextAppService.GetListAsync(new ErpNextInstanceListDto { MaxResultCount = 100 });
            return View(instances.Items);
        }

        // GET: /ErpNext/Details/{id}
        public async Task<IActionResult> Details(Guid id)
        {
            var instance = await _erpNextAppService.GetAsync(id);
            return View(instance);
        }

        // GET: /ErpNext/Create
        public IActionResult Create()
        {
            return View(new CreateErpNextInstanceDto());
        }

        // POST: /ErpNext/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(CreateErpNextInstanceDto input)
        {
            if (ModelState.IsValid)
            {
                await _erpNextAppService.CreateAsync(input);
                return RedirectToAction("Index");
            }
            return View(input);
        }

        // GET: /ErpNext/Edit/{id}
        public async Task<IActionResult> Edit(Guid id)
        {
            var instance = await _erpNextAppService.GetAsync(id);
            var updateDto = new UpdateErpNextInstanceDto
            {
                Name = instance.Name,
                BaseUrl = instance.BaseUrl,
                ApiKey = instance.ApiKey,
                ApiSecret = instance.ApiSecret,
                SiteName = instance.SiteName,
                IsActive = instance.IsActive,
                Description = instance.Description
            };
            ViewBag.InstanceId = id;
            ViewBag.InstanceName = instance.Name;
            return View(updateDto);
        }

        // POST: /ErpNext/Edit/{id}
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(Guid id, UpdateErpNextInstanceDto input)
        {
            if (ModelState.IsValid)
            {
                await _erpNextAppService.UpdateAsync(id, input);
                TempData["SuccessMessage"] = "ERPNext instance updated successfully.";
                return RedirectToAction("Details", new { id });
            }
            ViewBag.InstanceId = id;
            return View(input);
        }

        // POST: /ErpNext/Delete/{id}
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Delete(Guid id)
        {
            await _erpNextAppService.DeleteAsync(id);
            TempData["SuccessMessage"] = "ERPNext instance deleted successfully.";
            return RedirectToAction("Index");
        }

        // POST: /ErpNext/TestConnection/{id}
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> TestConnection(Guid id)
        {
            try
            {
                var result = await _erpNextAppService.TestConnectionAsync(id);
                TempData["SuccessMessage"] = $"Connection successful! Last sync: {result.LastSyncTime:yyyy-MM-dd HH:mm:ss}";
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Connection failed: {ex.Message}";
            }
            return RedirectToAction("Details", new { id });
        }
    }
}
