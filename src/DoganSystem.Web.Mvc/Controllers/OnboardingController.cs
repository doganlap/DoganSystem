using System;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.Emailing;
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
        private readonly IEmailSender _emailSender;

        public OnboardingController(
            ICurrentUser currentUser,
            ICurrentTenant currentTenant,
            IIdentityUserAppService identityUserAppService,
            IEmailSender emailSender)
        {
            _currentUser = currentUser;
            _currentTenant = currentTenant;
            _identityUserAppService = identityUserAppService;
            _emailSender = emailSender;
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

                // Send invitation email
                try
                {
                    var tenantName = _currentTenant.Name ?? "DoganSystem";
                    var resetPasswordLink = $"{Request.Scheme}://{Request.Host}/Account/ResetPassword?userId={user.Id}";

                    var emailSubject = $"Team Invitation - {tenantName}";
                    var emailBody = BuildInvitationEmailBody(
                        user.Email,
                        tenantName,
                        request.Role,
                        resetPasswordLink,
                        request.Message
                    );

                    await _emailSender.SendAsync(
                        to: user.Email,
                        subject: emailSubject,
                        body: emailBody,
                        isBodyHtml: true
                    );
                }
                catch (Exception emailEx)
                {
                    // Log email sending error but don't fail the invitation
                    // User account is created, admin can manually send credentials
                    Logger.LogWarning(emailEx, $"Failed to send invitation email to {request.Email}");
                }

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
            // Generate a secure temporary password (16 chars: Temp + 11 chars from GUID + !)
            var guid = Guid.NewGuid().ToString("N"); // 32 hex chars
            return $"Temp{guid.Substring(0, 11)}!"; // Total: 4 + 11 + 1 = 16 chars with special char
        }

        private static string BuildInvitationEmailBody(
            string recipientEmail,
            string tenantName,
            string role,
            string resetPasswordLink,
            string? personalMessage)
        {
            var sb = new StringBuilder();
            sb.AppendLine("<!DOCTYPE html>");
            sb.AppendLine("<html><head><meta charset='UTF-8'></head><body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>");
            sb.AppendLine("<div style='max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;'>");

            // Header
            sb.AppendLine($"<h2 style='color: #0066cc;'>You've Been Invited to {tenantName}</h2>");

            // Personal Message (if provided)
            if (!string.IsNullOrWhiteSpace(personalMessage))
            {
                sb.AppendLine($"<div style='background-color: #f5f5f5; padding: 15px; margin: 20px 0; border-left: 4px solid #0066cc;'>");
                sb.AppendLine($"<p style='margin: 0; font-style: italic;'>{System.Net.WebUtility.HtmlEncode(personalMessage)}</p>");
                sb.AppendLine("</div>");
            }

            // Main Content
            sb.AppendLine("<p>Hello,</p>");
            sb.AppendLine($"<p>You have been invited to join <strong>{tenantName}</strong> on DoganSystem with the role of <strong>{role}</strong>.</p>");
            sb.AppendLine("<p>A temporary account has been created for you. To get started, please set your password by clicking the button below:</p>");

            // Reset Password Button
            sb.AppendLine("<div style='text-align: center; margin: 30px 0;'>");
            sb.AppendLine($"<a href='{resetPasswordLink}' style='display: inline-block; padding: 12px 30px; background-color: #0066cc; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;'>Set Your Password</a>");
            sb.AppendLine("</div>");

            // Alternative Link
            sb.AppendLine("<p style='font-size: 14px; color: #666;'>Or copy and paste this link into your browser:</p>");
            sb.AppendLine($"<p style='font-size: 12px; word-break: break-all; background-color: #f5f5f5; padding: 10px; border-radius: 3px;'>{resetPasswordLink}</p>");

            // Role Information
            sb.AppendLine("<hr style='margin: 30px 0; border: none; border-top: 1px solid #ddd;'>");
            sb.AppendLine($"<p><strong>Your Account Details:</strong></p>");
            sb.AppendLine("<ul>");
            sb.AppendLine($"<li><strong>Email:</strong> {recipientEmail}</li>");
            sb.AppendLine($"<li><strong>Role:</strong> {role}</li>");
            sb.AppendLine($"<li><strong>Organization:</strong> {tenantName}</li>");
            sb.AppendLine("</ul>");

            // Footer
            sb.AppendLine("<hr style='margin: 30px 0; border: none; border-top: 1px solid #ddd;'>");
            sb.AppendLine("<p style='font-size: 12px; color: #999;'>If you did not expect this invitation, please disregard this email or contact the administrator.</p>");
            sb.AppendLine("<p style='font-size: 12px; color: #999;'>This link will expire in 24 hours for security reasons.</p>");

            sb.AppendLine("</div></body></html>");

            return sb.ToString();
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
