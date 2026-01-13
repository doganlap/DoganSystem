using DoganSystem.Modules.TenantManagement.Application.Dtos;
using FluentValidation;

namespace DoganSystem.Application.Validation
{
    /// <summary>
    /// Validation rules for CreateTenantDto following FluentValidation best practices
    /// </summary>
    public class CreateTenantDtoValidator : AbstractValidator<CreateTenantDto>
    {
        public CreateTenantDtoValidator()
        {
            RuleFor(x => x.Name)
                .NotEmpty()
                .WithMessage("Tenant name is required.")
                .MaximumLength(200)
                .WithMessage("Tenant name must not exceed 200 characters.")
                .Matches(@"^[a-zA-Z0-9\s\-_]+$")
                .WithMessage("Tenant name can only contain letters, numbers, spaces, hyphens, and underscores.");

            RuleFor(x => x.Subdomain)
                .NotEmpty()
                .When(x => string.IsNullOrEmpty(x.Domain))
                .WithMessage("Either subdomain or domain must be provided.")
                .MaximumLength(63)
                .WithMessage("Subdomain must not exceed 63 characters.")
                .Matches(@"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$")
                .WithMessage("Subdomain must be lowercase alphanumeric with hyphens, and cannot start or end with a hyphen.")
                .When(x => !string.IsNullOrEmpty(x.Subdomain));

            RuleFor(x => x.Domain)
                .MaximumLength(255)
                .WithMessage("Domain must not exceed 255 characters.")
                .Matches(@"^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$")
                .WithMessage("Domain must be a valid domain name.")
                .When(x => !string.IsNullOrEmpty(x.Domain));

            RuleFor(x => x.SubscriptionTier)
                .IsInEnum()
                .WithMessage("Invalid subscription tier.");

            RuleFor(x => x.TrialDays)
                .GreaterThanOrEqualTo(0)
                .WithMessage("Trial days must be greater than or equal to 0.")
                .LessThanOrEqualTo(365)
                .WithMessage("Trial days must not exceed 365 days.");
        }
    }
}
