using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class AssessmentsController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "التقييمات";
            return View();
        }
    }
}
