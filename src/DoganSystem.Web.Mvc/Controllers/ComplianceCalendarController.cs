using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class ComplianceCalendarController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "تقويم الامتثال";
            return View();
        }
    }
}
