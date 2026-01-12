using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class ControlAssessmentsController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "تقييمات الضوابط";
            return View();
        }
    }
}
