using System;
using System.ComponentModel.DataAnnotations;
using Volo.Abp.Domain.Entities.Auditing;

namespace DoganSystem.Core.Domain.Entities;

/// <summary>
/// Entity for storing contact form submissions from landing pages.
/// Uses ABP's FullAuditedEntity for complete audit trail.
/// </summary>
public class ContactSubmission : FullAuditedEntity<Guid>
{
    [Required]
    [MaxLength(100)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [MaxLength(200)]
    public string Email { get; set; } = string.Empty;

    [MaxLength(200)]
    public string? Company { get; set; }

    [MaxLength(50)]
    public string? ServiceInterest { get; set; }

    [Required]
    [MaxLength(2000)]
    public string Message { get; set; } = string.Empty;

    /// <summary>
    /// Status of the contact submission: New, InProgress, Completed, Archived
    /// </summary>
    [MaxLength(50)]
    public string Status { get; set; } = "New";

    /// <summary>
    /// User ID assigned to handle this contact
    /// </summary>
    public Guid? AssignedToUserId { get; set; }

    /// <summary>
    /// Internal notes about this contact
    /// </summary>
    [MaxLength(2000)]
    public string? Notes { get; set; }

    /// <summary>
    /// Scheduled follow-up date
    /// </summary>
    public DateTime? FollowUpDate { get; set; }

    /// <summary>
    /// ERPNext Lead ID if synced
    /// </summary>
    [MaxLength(100)]
    public string? ErpNextLeadId { get; set; }

    /// <summary>
    /// When this contact was synced to ERPNext
    /// </summary>
    public DateTime? SyncedToErpNextAt { get; set; }

    protected ContactSubmission() { }

    public ContactSubmission(
        Guid id,
        string name,
        string email,
        string message,
        string? company = null,
        string? serviceInterest = null)
        : base(id)
    {
        Name = name;
        Email = email;
        Message = message;
        Company = company;
        ServiceInterest = serviceInterest;
        Status = "New";
    }
}
