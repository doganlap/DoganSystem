using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class AuditsController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "إدارة المراجعة";
            return View();
        }
    }
}
