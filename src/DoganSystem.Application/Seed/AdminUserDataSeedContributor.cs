using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Identity;

namespace DoganSystem.Application.Seed
{
    public class AdminUserDataSeedContributor : IDataSeedContributor, ITransientDependency
    {
        private readonly IdentityUserManager _userManager;
        private readonly IdentityRoleManager _roleManager;
        private readonly ILogger<AdminUserDataSeedContributor> _logger;

        // Default admin credentials - CHANGE IN PRODUCTION
        private const string AdminUserName = "admin";
        private const string AdminEmail = "admin@dogansystem.local";
        private const string AdminPassword = "Admin@123456";
        private const string AdminRoleName = "admin";

        public AdminUserDataSeedContributor(
            IdentityUserManager userManager,
            IdentityRoleManager roleManager,
            ILogger<AdminUserDataSeedContributor> logger)
        {
            _userManager = userManager;
            _roleManager = roleManager;
            _logger = logger;
        }

        public async Task SeedAsync(DataSeedContext context)
        {
            await SeedAdminRoleAsync();
            await SeedAdminUserAsync();
        }

        private async Task SeedAdminRoleAsync()
        {
            var adminRole = await _roleManager.FindByNameAsync(AdminRoleName);
            if (adminRole == null)
            {
                adminRole = new IdentityRole(Guid.NewGuid(), AdminRoleName)
                {
                    IsDefault = false,
                    IsPublic = true,
                    IsStatic = true
                };

                var result = await _roleManager.CreateAsync(adminRole);
                if (result.Succeeded)
                {
                    _logger.LogInformation("Admin role created successfully");
                }
                else
                {
                    _logger.LogWarning("Failed to create admin role: {Errors}", string.Join(", ", result.Errors));
                }
            }
        }

        private async Task SeedAdminUserAsync()
        {
            var adminUser = await _userManager.FindByNameAsync(AdminUserName);
            if (adminUser == null)
            {
                adminUser = new IdentityUser(
                    Guid.NewGuid(),
                    AdminUserName,
                    AdminEmail
                )
                {
                    Name = "System Administrator"
                };

                var result = await _userManager.CreateAsync(adminUser, AdminPassword);
                if (result.Succeeded)
                {
                    _logger.LogInformation("Admin user created successfully");
                    _logger.LogInformation("========================================");
                    _logger.LogInformation("DEFAULT ADMIN CREDENTIALS:");
                    _logger.LogInformation("  Username: {UserName}", AdminUserName);
                    _logger.LogInformation("  Password: {Password}", AdminPassword);
                    _logger.LogInformation("========================================");

                    // Assign admin role
                    await _userManager.AddToRoleAsync(adminUser, AdminRoleName);
                    _logger.LogInformation("Admin role assigned to admin user");
                }
                else
                {
                    _logger.LogWarning("Failed to create admin user: {Errors}", string.Join(", ", result.Errors));
                }
            }
            else
            {
                _logger.LogInformation("Admin user already exists");
            }
        }
    }
}
