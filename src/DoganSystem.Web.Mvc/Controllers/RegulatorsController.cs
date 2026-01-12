using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class RegulatorsController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "الجهات التنظيمية";
            return View();
        }
    }
}
