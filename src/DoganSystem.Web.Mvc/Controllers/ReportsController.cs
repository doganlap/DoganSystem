using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class ReportsController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "التقارير والتحليلات";
            return View();
        }
    }
}
