using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class WorkflowController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "محرك سير العمل";
            return View();
        }
    }
}
