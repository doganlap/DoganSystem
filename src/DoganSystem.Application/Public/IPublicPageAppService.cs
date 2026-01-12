using System.Threading.Tasks;
using Volo.Abp.Application.Services;

namespace DoganSystem.Application.Public;

public interface IPublicPageAppService : IApplicationService
{
    Task<PublicPageInfoDto> GetHomePageInfoAsync();
    Task SubmitContactFormAsync(ContactFormDto input);
}

public class PublicPageInfoDto
{
    public string CompanyName { get; set; } = string.Empty;
    public string CompanyDescription { get; set; } = string.Empty;
    public string Headline { get; set; } = string.Empty;
    public string Tagline { get; set; } = string.Empty;
    public string PositioningStatement { get; set; } = string.Empty;
}
