using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Guids;
using Volo.Abp.Identity;
using Volo.Abp.MultiTenancy;

namespace DoganSystem.Application.Seed;

/// <summary>
/// Seeds initial host-level admin user and roles for the application.
/// This runs at application startup to ensure base data exists.
/// </summary>
public class DoganSystemDataSeedContributor : IDataSeedContributor, ITransientDependency
{
    private readonly IIdentityUserRepository _userRepository;
    private readonly IIdentityRoleRepository _roleRepository;
    private readonly IdentityUserManager _userManager;
    private readonly IdentityRoleManager _roleManager;
    private readonly ICurrentTenant _currentTenant;
    private readonly IGuidGenerator _guidGenerator;
    private readonly IConfiguration _configuration;
    private readonly ILogger<DoganSystemDataSeedContributor> _logger;

    public DoganSystemDataSeedContributor(
        IIdentityUserRepository userRepository,
        IIdentityRoleRepository roleRepository,
        IdentityUserManager userManager,
        IdentityRoleManager roleManager,
        ICurrentTenant currentTenant,
        IGuidGenerator guidGenerator,
        IConfiguration configuration,
        ILogger<DoganSystemDataSeedContributor> logger)
    {
        _userRepository = userRepository;
        _roleRepository = roleRepository;
        _userManager = userManager;
        _roleManager = roleManager;
        _currentTenant = currentTenant;
        _guidGenerator = guidGenerator;
        _configuration = configuration;
        _logger = logger;
    }

    public async Task SeedAsync(DataSeedContext context)
    {
        _logger.LogInformation("Starting DoganSystem data seeding...");

        // Only seed for host (null tenant) - each tenant gets their own admin via trial registration
        if (_currentTenant.Id != null)
        {
            _logger.LogInformation("Skipping data seeding for tenant {TenantId}", _currentTenant.Id);
            return;
        }

        // Seed roles first
        await SeedRolesAsync();

        // Seed admin user
        await SeedAdminUserAsync();

        _logger.LogInformation("DoganSystem data seeding completed successfully.");
    }

    private async Task SeedRolesAsync()
    {
        var adminRole = await _roleRepository.FindByNormalizedNameAsync("ADMIN");
        if (adminRole == null)
        {
            adminRole = new IdentityRole(_guidGenerator.Create(), "admin")
            {
                IsStatic = true,
                IsPublic = true
            };
            await _roleManager.CreateAsync(adminRole);
            _logger.LogInformation("Created 'admin' role");
        }

        var userRole = await _roleRepository.FindByNormalizedNameAsync("USER");
        if (userRole == null)
        {
            userRole = new IdentityRole(_guidGenerator.Create(), "user")
            {
                IsStatic = true,
                IsPublic = true
            };
            await _roleManager.CreateAsync(userRole);
            _logger.LogInformation("Created 'user' role");
        }
    }

    private async Task SeedAdminUserAsync()
    {
        var adminEmail = _configuration["Seed:AdminEmail"] ?? "admin@saudibusinessgate.com";
        var adminUserName = _configuration["Seed:AdminUserName"] ?? "admin";
        var adminPassword = _configuration["Seed:AdminPassword"] ?? Environment.GetEnvironmentVariable("DOGANSYSTEM_ADMIN_PASSWORD") ?? "Admin123!";

        var adminUser = await _userRepository.FindByNormalizedEmailAsync(adminEmail.ToUpperInvariant());
        if (adminUser == null)
        {
            adminUser = new IdentityUser(
                _guidGenerator.Create(),
                adminUserName,
                adminEmail
            )
            {
                Name = "System",
                Surname = "Administrator"
            };

            var result = await _userManager.CreateAsync(adminUser, adminPassword);
            if (result.Succeeded)
            {
                // Assign admin role
                await _userManager.AddToRoleAsync(adminUser, "admin");
                _logger.LogInformation("Created admin user: {Email}", adminEmail);
            }
            else
            {
                _logger.LogError("Failed to create admin user: {Errors}",
                    string.Join(", ", result.Errors.Select(e => e.Description)));
            }
        }
        else
        {
            _logger.LogInformation("Admin user already exists: {Email}", adminEmail);
        }
    }
}
