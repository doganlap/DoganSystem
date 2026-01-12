using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class ActionPlansController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "خطط العمل";
            return View();
        }
    }
}
