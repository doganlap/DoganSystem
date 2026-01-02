using DoganSystem.Application.Policy.PolicyModels;
using Microsoft.Extensions.Logging;

namespace DoganSystem.Application.Policy;

public class PolicyEnforcer : IPolicyEnforcer
{
    private readonly PolicyStore _policyStore;
    private readonly PolicyAuditLogger _auditLogger;
    private readonly ILogger<PolicyEnforcer> _logger;

    public PolicyEnforcer(
        PolicyStore policyStore,
        PolicyAuditLogger auditLogger,
        ILogger<PolicyEnforcer> logger)
    {
        _policyStore = policyStore;
        _auditLogger = auditLogger;
        _logger = logger;
    }

    public async Task EnforceAsync(PolicyContext ctx, CancellationToken ct = default)
    {
        var policy = _policyStore.LoadPolicy();
        var matchedRules = new List<string>();
        var decisions = new List<string>();

        // Check exceptions first
        var applicableExceptions = policy.Spec.Exceptions
            .Where(e => e.ExpiresAt == null || e.ExpiresAt > DateTime.UtcNow)
            .Where(e => MatchesException(e, ctx))
            .ToList();

        // Evaluate rules in priority order
        var sortedRules = policy.Spec.Rules
            .Where(r => r.Enabled)
            .OrderBy(r => r.Priority)
            .ThenBy(r => r.Id)
            .ToList();

        foreach (var rule in sortedRules)
        {
            // Skip if exception applies
            if (applicableExceptions.Any(e => e.RuleIds.Contains(rule.Id)))
            {
                continue;
            }

            if (MatchesRule(rule, ctx))
            {
                matchedRules.Add(rule.Id);
                decisions.Add(rule.Effect);

                // Apply mutations
                if (rule.Effect == "mutate" && rule.Mutations.Any())
                {
                    foreach (var mutation in rule.Mutations)
                    {
                        MutationApplier.ApplyMutation(ctx.Resource, mutation);
                    }
                    continue; // Continue evaluation after mutation
                }

                // Handle deny (short circuit if configured)
                if (rule.Effect == "deny")
                {
                    _auditLogger.LogViolation(ctx, rule.Id, rule.Message);
                    _auditLogger.LogDecision(ctx, "deny", matchedRules);

                    throw new PolicyViolationException(
                        rule.Id,
                        rule.Message,
                        rule.Remediation?.Hint ?? ""
                    );
                }

                // Handle audit
                if (rule.Effect == "audit")
                {
                    _auditLogger.LogDecision(ctx, "audit", new List<string> { rule.Id });
                }

                // Short circuit on allow if configured
                if (policy.Spec.Execution.ShortCircuit && rule.Effect == "allow")
                {
                    break;
                }
            }
        }

        // Apply conflict strategy
        var finalDecision = ApplyConflictStrategy(decisions, policy.Spec.Execution.ConflictStrategy, policy.Spec.DefaultEffect);

        if (finalDecision == "deny")
        {
            _auditLogger.LogDecision(ctx, "deny", matchedRules);
            throw new PolicyViolationException(
                matchedRules.FirstOrDefault() ?? "UNKNOWN",
                "Policy violation: Access denied",
                "Contact administrator for access"
            );
        }

        _auditLogger.LogDecision(ctx, finalDecision, matchedRules);
    }

    private bool MatchesRule(PolicyRule rule, PolicyContext ctx)
    {
        // Check resource type match
        if (rule.Match.Resource.Type != "*" && rule.Match.Resource.Type != ctx.ResourceType)
        {
            return false;
        }

        // Check environment match
        if (rule.Match.Environment != "*" && rule.Match.Environment != ctx.Environment)
        {
            return false;
        }

        // Check principal match
        if (rule.Match.Principal != null)
        {
            if (!string.IsNullOrEmpty(rule.Match.Principal.Id) && rule.Match.Principal.Id != ctx.PrincipalId)
            {
                return false;
            }

            if (rule.Match.Principal.Roles.Any() && 
                !rule.Match.Principal.Roles.Any(r => ctx.PrincipalRoles.Contains(r)))
            {
                return false;
            }
        }

        // Evaluate conditions
        if (rule.When.Any())
        {
            foreach (var condition in rule.When)
            {
                if (!EvaluateCondition(condition, ctx.Resource))
                {
                    return false;
                }
            }
        }

        return true;
    }

    private bool MatchesException(PolicyException exception, PolicyContext ctx)
    {
        return MatchesRule(new PolicyRule
        {
            Match = exception.Match
        }, ctx);
    }

    private bool EvaluateCondition(PolicyCondition condition, object resource)
    {
        var value = DotPathResolver.Resolve(resource, condition.Path);
        var conditionValue = condition.Value;

        return condition.Op.ToLower() switch
        {
            "exists" => value != null,
            "equals" => EqualsValues(value, conditionValue),
            "notEquals" => !EqualsValues(value, conditionValue),
            "in" => conditionValue is System.Collections.IEnumerable enumerable && 
                    enumerable.Cast<object>().Any(v => EqualsValues(value, v)),
            "notIn" => conditionValue is System.Collections.IEnumerable enumerable && 
                       !enumerable.Cast<object>().Any(v => EqualsValues(value, v)),
            "matches" => value?.ToString() is string str && 
                        conditionValue?.ToString() is string pattern && 
                        System.Text.RegularExpressions.Regex.IsMatch(str, pattern),
            "notMatches" => value?.ToString() is string str && 
                           conditionValue?.ToString() is string pattern && 
                           !System.Text.RegularExpressions.Regex.IsMatch(str, pattern),
            _ => false
        };
    }

    private string ApplyConflictStrategy(List<string> decisions, string strategy, string defaultEffect)
    {
        if (!decisions.Any())
            return defaultEffect;

        return strategy switch
        {
            "denyOverrides" => decisions.Contains("deny") ? "deny" : decisions.LastOrDefault() ?? defaultEffect,
            "allowOverrides" => decisions.Contains("allow") ? "allow" : decisions.LastOrDefault() ?? defaultEffect,
            "highestPriorityWins" => decisions.LastOrDefault() ?? defaultEffect,
            _ => defaultEffect
        };
    }

    private static bool EqualsValues(object? a, object? b)
    {
        if (a == null && b == null) return true;
        if (a == null || b == null) return false;
        return string.Equals(a.ToString(), b.ToString(), StringComparison.OrdinalIgnoreCase);
    }
}
