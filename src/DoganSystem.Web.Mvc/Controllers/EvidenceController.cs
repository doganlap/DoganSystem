using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class EvidenceController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "الأدلة";
            return View();
        }
    }
}
