namespace DoganSystem.Application.Policy.PolicyModels;

public class PolicyRule
{
    public string Id { get; set; } = string.Empty;
    public int Priority { get; set; }
    public string Description { get; set; } = string.Empty;
    public bool Enabled { get; set; } = true;
    public PolicyMatch Match { get; set; } = new();
    public List<PolicyCondition> When { get; set; } = new();
    public string Effect { get; set; } = "allow"; // allow/deny/audit/mutate
    public string Message { get; set; } = string.Empty;
    public string Severity { get; set; } = "medium";
    public List<PolicyMutation> Mutations { get; set; } = new();
    public PolicyRemediation? Remediation { get; set; }
}

public class PolicyMatch
{
    public PolicyResourceMatch Resource { get; set; } = new();
    public PolicyPrincipalMatch? Principal { get; set; }
    public string Environment { get; set; } = "*";
}

public class PolicyResourceMatch
{
    public string Type { get; set; } = string.Empty;
    public string Name { get; set; } = "*";
    public Dictionary<string, string> Labels { get; set; } = new();
}

public class PolicyPrincipalMatch
{
    public string? Id { get; set; }
    public List<string> Roles { get; set; } = new();
}

public class PolicyCondition
{
    public string Op { get; set; } = string.Empty; // exists/equals/notEquals/in/notIn/matches/notMatches
    public string Path { get; set; } = string.Empty;
    public object? Value { get; set; }
}

public class PolicyMutation
{
    public string Op { get; set; } = string.Empty; // set/remove/add
    public string Path { get; set; } = string.Empty;
    public object? Value { get; set; }
}

public class PolicyRemediation
{
    public string? Url { get; set; }
    public string? Hint { get; set; }
}
