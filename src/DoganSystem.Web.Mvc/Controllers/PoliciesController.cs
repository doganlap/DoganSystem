using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class PoliciesController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "إدارة السياسات";
            return View();
        }
    }
}
