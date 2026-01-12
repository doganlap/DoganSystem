using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class NotificationsController : AbpController
    {
        public IActionResult Index()
        {
            ViewData["Title"] = "الإشعارات";
            return View();
        }
    }
}
