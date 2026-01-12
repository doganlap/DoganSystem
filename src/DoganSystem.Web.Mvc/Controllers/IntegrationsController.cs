using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class IntegrationsController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "مركز التكامل";
            return View();
        }
    }
}
