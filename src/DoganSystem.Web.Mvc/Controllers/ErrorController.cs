using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class ErrorController : AbpController
    {
        [Route("/Error")]
        public IActionResult Error()
        {
            return View();
        }
    }
}
