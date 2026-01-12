using DoganSystem.Localization;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Volo.Abp.Localization;
using Volo.Abp.Localization.ExceptionHandling;
using Volo.Abp.Modularity;
using Volo.Abp.Authorization;
using Volo.Abp.VirtualFileSystem;

namespace DoganSystem.Core
{
    [DependsOn(
        typeof(AbpAuthorizationModule),
        typeof(AbpLocalizationModule),
        typeof(AbpVirtualFileSystemModule)
    )]
    public class DoganSystemCoreModule : AbpModule
    {
        // Language display names mapping (not culture-specific, just display labels)
        private static readonly Dictionary<string, string> LanguageDisplayNames = new()
        {
            { "ar", "العربية" },
            { "en", "English" },
            { "fr", "Français" },
            { "de", "Deutsch" },
            { "es", "Español" },
            { "tr", "Türkçe" },
            { "zh", "中文" },
            { "ja", "日本語" }
        };

        public override void ConfigureServices(ServiceConfigurationContext context)
        {
            var configuration = context.Services.GetConfiguration();

            Configure<AbpVirtualFileSystemOptions>(options =>
            {
                options.FileSets.AddEmbedded<DoganSystemCoreModule>("DoganSystem.Core");
            });

            Configure<AbpLocalizationOptions>(options =>
            {
                // Read configuration - no hardcoding
                var defaultLanguage = configuration["Abp:Localization:DefaultLanguage"] ?? "ar";
                var supportedLanguages = configuration.GetSection("Abp:Localization:SupportedLanguages").Get<string[]>()
                    ?? new[] { "ar", "en" };

                // Add GrcResource with default culture from configuration
                var resourceBuilder = options.Resources.Add<GrcResource>(defaultLanguage);

                // Dynamically add virtual JSON paths for all supported languages
                foreach (var lang in supportedLanguages)
                {
                    resourceBuilder.AddVirtualJson($"/Localization/Resources/{lang}");
                }

                options.DefaultResourceType = typeof(GrcResource);

                // ABP 8.x LanguageInfo constructor: (cultureName, uiCultureName, displayName)
                // Add languages in order from configuration (first = default)
                foreach (var lang in supportedLanguages)
                {
                    var displayName = LanguageDisplayNames.GetValueOrDefault(lang, lang);
                    options.Languages.Add(new LanguageInfo(lang, lang, displayName));
                }
            });

            Configure<AbpExceptionLocalizationOptions>(options =>
            {
                options.MapCodeNamespace("DoganSystem", typeof(GrcResource));
            });
        }
    }
}
