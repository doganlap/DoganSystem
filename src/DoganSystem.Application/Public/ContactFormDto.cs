using System.ComponentModel.DataAnnotations;

namespace DoganSystem.Application.Public;

public class ContactFormDto
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(100)]
    [Display(Name = "Name")]
    public string Name { get; set; } = string.Empty;

    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Invalid email address")]
    [StringLength(200)]
    [Display(Name = "Email")]
    public string Email { get; set; } = string.Empty;

    [StringLength(200)]
    [Display(Name = "Company")]
    public string? Company { get; set; }

    [Display(Name = "Service Interest")]
    public string? ServiceInterest { get; set; }

    [Required(ErrorMessage = "Message is required")]
    [StringLength(2000)]
    [Display(Name = "Message")]
    public string Message { get; set; } = string.Empty;
}
