using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class FrameworksController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "مكتبة الأطر التنظيمية";
            return View();
        }
    }
}
