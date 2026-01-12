using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc.UI.Theming;
using DoganSystem.Constants;
using DoganSystem.Application.Public;

namespace DoganSystem.Web.Mvc.Controllers
{
    [AllowAnonymous] // Make all actions public (no authentication required)
    public class PublicController : AbpController
    {
        private readonly IPublicPageAppService _publicPageAppService;

        public PublicController(IPublicPageAppService publicPageAppService)
        {
            _publicPageAppService = publicPageAppService;
        }

        /// <summary>
        /// Landing page - Public homepage
        /// </summary>
        public async Task<IActionResult> Index()
        {
            // #region agent log
            try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "B", location = "PublicController.cs:Index", message = "Index action entry", data = new { }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
            // #endregion
            try
            {
                // #region agent log
                try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "B", location = "PublicController.cs:Index", message = "Before GetHomePageInfoAsync", data = new { }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
                // #endregion
                var pageInfo = await _publicPageAppService.GetHomePageInfoAsync();
                // #region agent log
                try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "B", location = "PublicController.cs:Index", message = "After GetHomePageInfoAsync", data = new { companyName = pageInfo?.CompanyName }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
                // #endregion
                ViewBag.AppName = pageInfo.CompanyName;
                ViewBag.AppDescription = pageInfo.CompanyDescription;
                ViewBag.Headline = pageInfo.Headline;
                ViewBag.Tagline = pageInfo.Tagline;
                ViewBag.Positioning = pageInfo.PositioningStatement;
                // #region agent log
                try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "B", location = "PublicController.cs:Index", message = "Before return View", data = new { }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
                // #endregion
                return View();
            }
            catch (Exception ex)
            {
                // #region agent log
                try { System.IO.File.AppendAllText("/root/CascadeProjects/DoganSystem/.cursor/debug.log", System.Text.Json.JsonSerializer.Serialize(new { sessionId = "debug-session", runId = "run1", hypothesisId = "A", location = "PublicController.cs:Index", message = "Index action EXCEPTION", data = new { exceptionType = ex.GetType().Name, message = ex.Message, stackTrace = ex.StackTrace != null ? ex.StackTrace.Substring(0, Math.Min(200, ex.StackTrace.Length)) : null }, timestamp = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() }) + "\n"); } catch { }
                // #endregion
                throw;
            }
        }

        /// <summary>
        /// About page - Company information
        /// </summary>
        public IActionResult About()
        {
            ViewBag.CompanyName = BrandMessages.CompanyName;
            ViewBag.Tagline = BrandMessages.TaglinePrimary;
            return View();
        }

        /// <summary>
        /// Services page - Services offered
        /// </summary>
        public IActionResult Services()
        {
            ViewBag.CompanyName = BrandMessages.CompanyName;
            return View();
        }

        /// <summary>
        /// Industries page - Target sectors
        /// </summary>
        public IActionResult Industries()
        {
            ViewBag.CompanyName = BrandMessages.CompanyName;
            return View();
        }

        /// <summary>
        /// Credentials & Expertise page - Case studies, certifications
        /// </summary>
        public IActionResult Credentials()
        {
            ViewBag.CompanyName = BrandMessages.CompanyName;
            return View();
        }

        /// <summary>
        /// Insights/Resources page - Whitepapers, blog, resources
        /// </summary>
        public IActionResult Insights()
        {
            ViewBag.CompanyName = BrandMessages.CompanyName;
            return View();
        }

        /// <summary>
        /// Contact page - Contact form
        /// </summary>
        public IActionResult Contact()
        {
            ViewBag.CompanyName = BrandMessages.CompanyName;
            return View(new ContactFormDto());
        }

        /// <summary>
        /// Pricing page - Consulting engagement models
        /// </summary>
        public IActionResult Pricing()
        {
            ViewBag.CompanyName = BrandMessages.CompanyName;
            return View();
        }

        /// <summary>
        /// Features page - Consulting capabilities
        /// </summary>
        public IActionResult Features()
        {
            ViewBag.CompanyName = BrandMessages.CompanyName;
            return View();
        }

        /// <summary>
        /// Handle contact form submission
        /// </summary>
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Contact(ContactFormDto input)
        {
            if (!ModelState.IsValid)
            {
                ViewBag.CompanyName = BrandMessages.CompanyName;
                return View(input);
            }

            await _publicPageAppService.SubmitContactFormAsync(input);
            
            TempData["SuccessMessage"] = "تم إرسال رسالتك بنجاح. سنتواصل معك قريباً.";
            return RedirectToAction(nameof(Contact));
        }
    }
}
