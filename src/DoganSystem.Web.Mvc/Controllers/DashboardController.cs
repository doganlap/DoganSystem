using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;
using DoganSystem.Permissions;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class DashboardController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "لوحة التحكم";
            return View();
        }
    }
}
