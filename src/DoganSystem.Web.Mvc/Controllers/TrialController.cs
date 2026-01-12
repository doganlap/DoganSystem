using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Volo.Abp;
using Volo.Abp.AspNetCore.Mvc;
using Volo.Abp.Identity;
using Volo.Abp.MultiTenancy;
using Volo.Abp.TenantManagement;
using Volo.Abp.Application.Dtos;
using DoganSystem.Modules.TenantManagement.Application;
using DoganSystem.Modules.TenantManagement.Application.Dtos;

namespace DoganSystem.Web.Mvc.Controllers
{
    /// <summary>
    /// Trial registration controller using ABP services
    /// </summary>
    [AllowAnonymous]
    public class TrialController : AbpController
    {
        private readonly Volo.Abp.TenantManagement.ITenantAppService _abpTenantAppService;
        private readonly DoganSystem.Modules.TenantManagement.Application.ITenantAppService _customTenantAppService;
        private readonly IIdentityUserAppService _identityUserAppService;
        private readonly ICurrentTenant _currentTenant;

        public TrialController(
            Volo.Abp.TenantManagement.ITenantAppService abpTenantAppService,
            DoganSystem.Modules.TenantManagement.Application.ITenantAppService customTenantAppService,
            IIdentityUserAppService identityUserAppService,
            ICurrentTenant currentTenant)
        {
            _abpTenantAppService = abpTenantAppService;
            _customTenantAppService = customTenantAppService;
            _identityUserAppService = identityUserAppService;
            _currentTenant = currentTenant;
        }

        /// <summary>
        /// Trial registration form page
        /// </summary>
        [HttpGet]
        [Route("/Trial/Register")]
        public IActionResult Register()
        {
            return View();
        }

        /// <summary>
        /// Trial registration success page
        /// </summary>
        [HttpGet]
        [Route("/Trial/Success")]
        public IActionResult Success([FromQuery] string tenant, [FromQuery] string email)
        {
            ViewBag.TenantName = tenant;
            ViewBag.Email = email;
            return View();
        }

        /// <summary>
        /// Register a new trial tenant with admin user
        /// </summary>
        [HttpPost]
        [Route("/api/trial/register")]
        public async Task<IActionResult> RegisterTrial([FromBody] RegisterTrialRequest request)
        {
            try
            {
                // Create tenant using ABP TenantManagement service
                // Use dynamic object to avoid compile-time dependency on ABP DTOs
                dynamic abpCreateDto = new System.Dynamic.ExpandoObject();
                abpCreateDto.Name = request.CompanyName;
                abpCreateDto.AdminEmailAddress = request.AdminEmail;
                abpCreateDto.AdminPassword = request.AdminPassword;
                
                dynamic abpTenant = await _abpTenantAppService.CreateAsync(abpCreateDto);

                // Create custom tenant with extended properties (if needed for additional metadata)
                var customTenantDto = new CreateTenantDto
                {
                    Name = request.CompanyName,
                    Subdomain = request.Subdomain,
                    Domain = request.Subdomain,
                    SubscriptionTier = "Starter",
                    TrialDays = request.TrialDays,
                    Metadata = null
                };

                var customTenant = await _customTenantAppService.CreateAsync(customTenantDto);

                // ABP's CreateTenantAsync automatically creates the admin user
                // Switch to the new tenant context to get admin user details
                using (_currentTenant.Change(abpTenant.Id))
                {
                    // Get users list and find the admin user by email
                    var users = await _identityUserAppService.GetListAsync(new GetIdentityUsersInput
                    {
                        Filter = request.AdminEmail
                    });

                    var adminUser = users.Items.FirstOrDefault(u => u.Email == request.AdminEmail);

                    // If admin user exists (created by ABP), update additional info if needed
                    if (adminUser != null && (!string.IsNullOrEmpty(request.AdminName) || !string.IsNullOrEmpty(request.AdminPhone)))
                    {
                        var updateDto = new IdentityUserUpdateDto
                        {
                            UserName = adminUser.UserName,
                            Email = adminUser.Email,
                            Name = request.AdminName ?? adminUser.Name,
                            Surname = request.AdminSurname ?? adminUser.Surname,
                            PhoneNumber = request.AdminPhone ?? adminUser.PhoneNumber,
                            LockoutEnabled = adminUser.LockoutEnabled
                        };
                        await _identityUserAppService.UpdateAsync(adminUser.Id, updateDto);
                        adminUser = await _identityUserAppService.GetAsync(adminUser.Id);
                    }

                    return Ok(new RegisterTrialResponse
                    {
                        Success = true,
                        TenantId = abpTenant.Id,
                        TenantName = abpTenant.Name,
                        AdminUserId = adminUser?.Id,
                        Message = "Trial registration successful. Please log in to continue."
                    });
                }
            }
            catch (UserFriendlyException ex)
            {
                return BadRequest(new RegisterTrialResponse
                {
                    Success = false,
                    Message = ex.Message
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new RegisterTrialResponse
                {
                    Success = false,
                    Message = "An error occurred during trial registration: " + ex.Message
                });
            }
        }

        /// <summary>
        /// Check if subdomain is available
        /// </summary>
        [HttpGet]
        [Route("/api/trial/check-subdomain")]
        public async Task<IActionResult> CheckSubdomain([FromQuery] string subdomain)
        {
            try
            {
                // Check subdomain availability using custom tenant service
                var customTenants = await _customTenantAppService.GetListAsync(new TenantListDto
                {
                    Filter = subdomain
                });
                
                // Also check ABP tenants if needed
                dynamic abpInput = new System.Dynamic.ExpandoObject();
                abpInput.Filter = subdomain;
                dynamic abpTenants = await _abpTenantAppService.GetListAsync(abpInput);

                var isAvailable = customTenants.TotalCount == 0 && ((PagedResultDto<object>)abpTenants).TotalCount == 0;
                return Ok(new { available = isAvailable });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }
    }

    public class RegisterTrialRequest
    {
        public string CompanyName { get; set; }
        public string Subdomain { get; set; }
        public string AdminEmail { get; set; }
        public string AdminPassword { get; set; }
        public string AdminUserName { get; set; }
        public string AdminName { get; set; }
        public string AdminSurname { get; set; }
        public string AdminPhone { get; set; }
        public int TrialDays { get; set; } = 14;
    }

    public class RegisterTrialResponse
    {
        public bool Success { get; set; }
        public Guid? TenantId { get; set; }
        public string TenantName { get; set; }
        public Guid? AdminUserId { get; set; }
        public string Message { get; set; }
    }
}
