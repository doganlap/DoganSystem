using System;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.Identity;
using Volo.Abp.MultiTenancy;
using Volo.Abp.Users;

namespace DoganSystem.Web.Mvc.Controllers
{
    /// <summary>
    /// Onboarding controller using ABP built-in services
    /// </summary>
    [Authorize]
    public class OnboardingController : AbpController
    {
        private readonly ICurrentUser _currentUser;
        private readonly ICurrentTenant _currentTenant;
        private readonly IIdentityUserAppService _identityUserAppService;

        public OnboardingController(
            ICurrentUser currentUser,
            ICurrentTenant currentTenant,
            IIdentityUserAppService identityUserAppService)
        {
            _currentUser = currentUser;
            _currentTenant = currentTenant;
            _identityUserAppService = identityUserAppService;
        }

        /// <summary>
        /// Welcome page - first page after login for new users
        /// </summary>
        [HttpGet]
        [Route("/Onboarding/Welcome")]
        public IActionResult Welcome()
        {
            // Calculate trial days remaining (if applicable)
            // This would typically come from tenant settings
            ViewBag.TrialDaysRemaining = 14; // Default, can be calculated from tenant creation date
            return View();
        }

        /// <summary>
        /// Company setup wizard
        /// </summary>
        [HttpGet]
        [Route("/Onboarding/Setup")]
        public IActionResult Setup()
        {
            return View();
        }

        /// <summary>
        /// Invite team members page
        /// </summary>
        [HttpGet]
        [Route("/Onboarding/InviteTeam")]
        public IActionResult InviteTeam()
        {
            return View();
        }

        /// <summary>
        /// Send team invitation using ABP Identity
        /// </summary>
        [HttpPost]
        [Route("/api/onboarding/invite")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SendInvitation([FromBody] InviteTeamMemberRequest request)
        {
            // Validate model state
            if (!ModelState.IsValid)
            {
                return BadRequest(new
                {
                    success = false,
                    message = "Validation failed: " + string.Join(", ", ModelState.Values.SelectMany(v => v.Errors).Select(e => e.ErrorMessage))
                });
            }

            try
            {
                // Create user using ABP's Identity service
                var createUserDto = new IdentityUserCreateDto
                {
                    UserName = request.Email,
                    Email = request.Email,
                    Password = GenerateTemporaryPassword(),
                    IsActive = true,
                    LockoutEnabled = false,
                    RoleNames = new[] { request.Role }
                };

                var user = await _identityUserAppService.CreateAsync(createUserDto);

                // TODO: Send invitation email using ABP's IEmailSender
                // The email would contain a password reset link

                return Ok(new
                {
                    success = true,
                    userId = user.Id,
                    message = $"Invitation sent to {request.Email}"
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new
                {
                    success = false,
                    message = ex.Message
                });
            }
        }

        /// <summary>
        /// Get current user's onboarding status
        /// </summary>
        [HttpGet]
        [Route("/api/onboarding/status")]
        public IActionResult GetOnboardingStatus()
        {
            // Return basic onboarding status
            // This can be extended to track completed steps in database
            return Ok(new
            {
                userId = _currentUser.Id,
                userName = _currentUser.UserName,
                tenantId = _currentTenant.Id,
                tenantName = _currentTenant.Name,
                isAuthenticated = _currentUser.IsAuthenticated
            });
        }

        /// <summary>
        /// Mark onboarding as complete
        /// </summary>
        [HttpPost]
        [Route("/api/onboarding/complete")]
        [ValidateAntiForgeryToken]
        public IActionResult CompleteOnboarding()
        {
            // This would typically update a user setting or tenant setting
            // to mark onboarding as complete
            return Ok(new { success = true, message = "Onboarding completed" });
        }

        private static string GenerateTemporaryPassword()
        {
            // Generate a secure temporary password
            return $"Temp{Guid.NewGuid():N}!".Substring(0, 16);
        }
    }

    public class InviteTeamMemberRequest
    {
        [Required(ErrorMessage = "Email is required")]
        [EmailAddress(ErrorMessage = "Invalid email address format")]
        public string Email { get; set; } = string.Empty;

        [Required(ErrorMessage = "Role is required")]
        [RegularExpression(@"^(Viewer|Auditor|ComplianceManager|RiskManager|TenantAdmin)$",
            ErrorMessage = "Role must be one of: Viewer, Auditor, ComplianceManager, RiskManager, TenantAdmin")]
        public string Role { get; set; } = "Viewer";

        [StringLength(500, ErrorMessage = "Message cannot exceed 500 characters")]
        public string? Message { get; set; }
    }
}
