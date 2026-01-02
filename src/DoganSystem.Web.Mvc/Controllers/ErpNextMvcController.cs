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

        public async Task<IActionResult> Index()
        {
            var instances = await _erpNextAppService.GetListAsync(new ErpNextInstanceListDto { MaxResultCount = 100 });
            return View(instances.Items);
        }

        public async Task<IActionResult> Details(Guid id)
        {
            var instance = await _erpNextAppService.GetAsync(id);
            return View(instance);
        }

        public IActionResult Create()
        {
            return View(new CreateErpNextInstanceDto());
        }

        [HttpPost]
        public async Task<IActionResult> Create(CreateErpNextInstanceDto input)
        {
            if (ModelState.IsValid)
            {
                await _erpNextAppService.CreateAsync(input);
                return RedirectToAction("Index");
            }
            return View(input);
        }
    }
}
