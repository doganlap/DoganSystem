using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class VendorsController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "إدارة الموردين";
            return View();
        }
    }
}
