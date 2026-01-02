using Microsoft.Extensions.Logging;

namespace DoganSystem.Application.Policy;

public class PolicyAuditLogger
{
    private readonly ILogger<PolicyAuditLogger> _logger;

    public PolicyAuditLogger(ILogger<PolicyAuditLogger> logger)
    {
        _logger = logger;
    }

    public void LogDecision(PolicyContext context, string decision, List<string> matchedRules)
    {
        _logger.LogInformation(
            "POLICY_DECISION: User={UserId}, Tenant={TenantId}, Action={Action}, ResourceType={ResourceType}, Decision={Decision}, MatchedRules={MatchedRules}, Timestamp={Timestamp}",
            context.PrincipalId,
            context.TenantId,
            context.Action,
            context.ResourceType,
            decision,
            string.Join(",", matchedRules),
            DateTime.UtcNow
        );
    }

    public void LogViolation(PolicyContext context, string ruleId, string message)
    {
        _logger.LogWarning(
            "POLICY_VIOLATION: User={UserId}, Tenant={TenantId}, Action={Action}, ResourceType={ResourceType}, RuleId={RuleId}, Message={Message}, Timestamp={Timestamp}",
            context.PrincipalId,
            context.TenantId,
            context.Action,
            context.ResourceType,
            ruleId,
            message,
            DateTime.UtcNow
        );
    }
}
