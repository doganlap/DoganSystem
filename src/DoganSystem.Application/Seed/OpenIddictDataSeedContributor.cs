using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Volo.Abp;
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;
using Volo.Abp.OpenIddict;
using OpenIddict.Abstractions;

namespace DoganSystem.Application.Seed
{
    /// <summary>
    /// Seed data contributor for OpenIddict applications and scopes
    /// Disabled - using Azure AD for authentication instead
    /// </summary>
    // [TransientDependency] // Commented out - OpenIddict removed
    public class OpenIddictDataSeedContributor // : IDataSeedContributor, ITransientDependency // Disabled
    {
        private readonly IConfiguration _configuration;
        private readonly IOpenIddictApplicationManager _applicationManager;
        private readonly IOpenIddictScopeManager _scopeManager;

        public OpenIddictDataSeedContributor(
            IConfiguration configuration,
            IOpenIddictApplicationManager applicationManager,
            IOpenIddictScopeManager scopeManager)
        {
            _configuration = configuration;
            _applicationManager = applicationManager;
            _scopeManager = scopeManager;
        }

        public async Task SeedAsync(DataSeedContext context)
        {
            // Seed OpenIddict scopes
            await SeedScopesAsync(context);

            // Seed OpenIddict applications
            await SeedApplicationsAsync(context);
        }

        private async Task SeedScopesAsync(DataSeedContext context)
        {
            var scopesSection = _configuration.GetSection("OpenIddict:Resources:DoganSystem:Scopes");
            if (!scopesSection.Exists())
                return;

            var scopes = scopesSection.Get<string[]>();
            if (scopes == null || scopes.Length == 0)
                return;

            foreach (var scopeName in scopes)
            {
                var scope = await _scopeManager.FindByNameAsync(scopeName);
                if (scope == null)
                {
                    await _scopeManager.CreateAsync(new OpenIddictScopeDescriptor
                    {
                        Name = scopeName,
                        DisplayName = scopeName,
                        Resources = { "DoganSystem" }
                    });
                }
            }
        }

        private async Task SeedApplicationsAsync(DataSeedContext context)
        {
            var applicationsSection = _configuration.GetSection("OpenIddict:Applications");
            if (!applicationsSection.Exists())
                return;

            foreach (var appSection in applicationsSection.GetChildren())
            {
                var clientId = appSection.Key;
                var clientSecret = appSection["ClientSecret"] ?? string.Empty;
                var rootUrl = appSection["RootUrl"] ?? string.Empty;
                var scopes = appSection.GetSection("Scopes").Get<string[]>() ?? Array.Empty<string>();
                var grantTypes = appSection.GetSection("GrantTypes").Get<string[]>() ?? Array.Empty<string>();
                var redirectUris = appSection.GetSection("RedirectUris").Get<string[]>() ?? Array.Empty<string>();
                var postLogoutRedirectUris = appSection.GetSection("PostLogoutRedirectUris").Get<string[]>() ?? Array.Empty<string>();

                var application = await _applicationManager.FindByClientIdAsync(clientId);
                if (application == null)
                {
                    var descriptor = new OpenIddictApplicationDescriptor
                    {
                        ClientId = clientId,
                        DisplayName = clientId,
                        ClientType = OpenIddictConstants.ClientTypes.Confidential
                    };

                    if (!string.IsNullOrEmpty(clientSecret))
                    {
                        descriptor.ClientSecret = clientSecret;
                    }

                    foreach (var scope in scopes)
                    {
                        descriptor.Permissions.Add(OpenIddictConstants.Permissions.Prefixes.Scope + scope);
                    }

                    foreach (var grantType in grantTypes)
                    {
                        descriptor.Permissions.Add(OpenIddictConstants.Permissions.Prefixes.GrantType + grantType);
                    }

                    foreach (var redirectUri in redirectUris)
                    {
                        if (Uri.TryCreate(redirectUri, UriKind.Absolute, out var uri))
                        {
                            descriptor.RedirectUris.Add(uri);
                        }
                    }

                    foreach (var postLogoutRedirectUri in postLogoutRedirectUris)
                    {
                        if (Uri.TryCreate(postLogoutRedirectUri, UriKind.Absolute, out var uri))
                        {
                            descriptor.PostLogoutRedirectUris.Add(uri);
                        }
                    }

                    await _applicationManager.CreateAsync(descriptor);
                }
            }
        }
    }
}
