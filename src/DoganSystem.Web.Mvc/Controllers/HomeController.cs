using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Volo.Abp.AspNetCore.Mvc;
using DoganSystem.Application.Public;

namespace DoganSystem.Web.Mvc.Controllers
{
    public class HomeController : AbpController
    {
        private readonly IPublicPageAppService _publicPageAppService;

        public HomeController(IPublicPageAppService publicPageAppService)
        {
            _publicPageAppService = publicPageAppService;
        }

        /// <summary>
        /// Landing page at root - redirects to Public landing page
        /// </summary>
        [AllowAnonymous]
        public async Task<ActionResult> Index()
        {
            // Serve the landing page at root
            var pageInfo = await _publicPageAppService.GetHomePageInfoAsync();
            ViewBag.AppName = pageInfo.CompanyName;
            ViewBag.AppDescription = pageInfo.CompanyDescription;
            ViewBag.Headline = pageInfo.Headline;
            ViewBag.Tagline = pageInfo.Tagline;
            ViewBag.Positioning = pageInfo.PositioningStatement;
            return View();
        }

        /// <summary>
        /// Dashboard page - for authenticated users
        /// </summary>
        [Route("dashboard")]
        public ActionResult Dashboard()
        {
            return View();
        }

        /// <summary>
        /// Health check endpoint for Docker/Kubernetes
        /// </summary>
        [AllowAnonymous]
        [Route("health")]
        [HttpGet]
        public ActionResult Health()
        {
            return Ok(new
            {
                status = "healthy",
                service = "DoganSystem.Web.Mvc",
                version = "2.0.0",
                timestamp = DateTime.UtcNow,
                environment = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production"
            });
        }
    }
}
