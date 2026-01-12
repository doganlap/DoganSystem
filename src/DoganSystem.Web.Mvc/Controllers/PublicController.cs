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
            var pageInfo = await _publicPageAppService.GetHomePageInfoAsync();
            if (pageInfo != null)
            {
                ViewBag.AppName = pageInfo.CompanyName;
                ViewBag.AppDescription = pageInfo.CompanyDescription;
                ViewBag.Headline = pageInfo.Headline;
                ViewBag.Tagline = pageInfo.Tagline;
                ViewBag.Positioning = pageInfo.PositioningStatement;
            }
            return View();
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
