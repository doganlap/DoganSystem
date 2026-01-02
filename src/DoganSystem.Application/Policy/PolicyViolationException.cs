using Volo.Abp;

namespace DoganSystem.Application.Policy;

public class PolicyViolationException : BusinessException
{
    public string RuleId { get; }
    public string RemediationHint { get; }

    public PolicyViolationException(string ruleId, string message, string remediationHint = "")
        : base("Grc:PolicyViolation", message)
    {
        RuleId = ruleId;
        RemediationHint = remediationHint;
    }
}
