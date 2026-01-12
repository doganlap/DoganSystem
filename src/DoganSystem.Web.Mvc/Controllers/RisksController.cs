using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class RisksController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "إدارة المخاطر";
            return View();
        }
    }
}
