namespace DoganSystem.Application.Policy.PolicyModels;

public class PolicyDocument
{
    public string ApiVersion { get; set; } = "policy.doganconsult.io/v1";
    public string Kind { get; set; } = "Policy";
    public PolicyMetadata Metadata { get; set; } = new();
    public PolicySpec Spec { get; set; } = new();
}

public class PolicyMetadata
{
    public string Name { get; set; } = string.Empty;
    public string Namespace { get; set; } = "default";
    public string Version { get; set; } = "1.0.0";
    public DateTime CreatedAt { get; set; }
    public Dictionary<string, string> Labels { get; set; } = new();
    public Dictionary<string, string> Annotations { get; set; } = new();
}

public class PolicySpec
{
    public string Mode { get; set; } = "enforce"; // enforce/audit
    public string DefaultEffect { get; set; } = "allow";
    public PolicyExecution Execution { get; set; } = new();
    public PolicyTarget Target { get; set; } = new();
    public List<PolicyRule> Rules { get; set; } = new();
    public List<PolicyException> Exceptions { get; set; } = new();
    public PolicyAudit? Audit { get; set; }
}

public class PolicyExecution
{
    public string Order { get; set; } = "sequential";
    public bool ShortCircuit { get; set; } = true;
    public string ConflictStrategy { get; set; } = "denyOverrides"; // denyOverrides/allowOverrides/highestPriorityWins
}

public class PolicyTarget
{
    public List<string> ResourceTypes { get; set; } = new();
    public List<string> Environments { get; set; } = new();
}

public class PolicyException
{
    public string Id { get; set; } = string.Empty;
    public List<string> RuleIds { get; set; } = new();
    public string Reason { get; set; } = string.Empty;
    public DateTime? ExpiresAt { get; set; }
    public PolicyMatch Match { get; set; } = new();
}

public class PolicyAudit
{
    public bool LogDecisions { get; set; } = true;
    public int RetentionDays { get; set; } = 365;
    public List<PolicyAuditSink> Sinks { get; set; } = new();
}

public class PolicyAuditSink
{
    public string Type { get; set; } = string.Empty; // stdout/file/http
    public string? Path { get; set; }
    public string? Url { get; set; }
    public Dictionary<string, string> Headers { get; set; } = new();
}
