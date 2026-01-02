using System.Text.Json;
using DoganSystem.Application.Policy.PolicyModels;
using YamlDotNet.Serialization;
using Microsoft.Extensions.Logging;

namespace DoganSystem.Application.Policy;

public class PolicyStore
{
    private readonly ILogger<PolicyStore> _logger;
    private PolicyDocument? _cachedPolicy;
    private DateTime? _lastLoadTime;
    private readonly string _policyFilePath;

    public PolicyStore(ILogger<PolicyStore> logger, string policyFilePath = "etc/policies/grc-baseline.yml")
    {
        _logger = logger;
        _policyFilePath = policyFilePath;
    }

    public PolicyDocument LoadPolicy()
    {
        // Cache policy for 5 minutes
        if (_cachedPolicy != null && _lastLoadTime.HasValue && 
            DateTime.UtcNow - _lastLoadTime.Value < TimeSpan.FromMinutes(5))
        {
            return _cachedPolicy;
        }

        try
        {
            if (!File.Exists(_policyFilePath))
            {
                _logger.LogWarning("Policy file not found at {Path}, using default policy", _policyFilePath);
                return GetDefaultPolicy();
            }

            var yamlContent = File.ReadAllText(_policyFilePath);
            var deserializer = new DeserializerBuilder().Build();
            var yamlObject = deserializer.Deserialize<Dictionary<object, object>>(yamlContent);

            // Convert to JSON then deserialize to PolicyDocument
            var serializer = new SerializerBuilder().JsonCompatible().Build();
            var json = serializer.Serialize(yamlObject);
            var policy = JsonSerializer.Deserialize<PolicyDocument>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            if (policy == null)
            {
                _logger.LogWarning("Failed to deserialize policy, using default");
                return GetDefaultPolicy();
            }

            _cachedPolicy = policy;
            _lastLoadTime = DateTime.UtcNow;
            return policy;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error loading policy file, using default policy");
            return GetDefaultPolicy();
        }
    }

    private PolicyDocument GetDefaultPolicy()
    {
        return new PolicyDocument
        {
            ApiVersion = "policy.doganconsult.io/v1",
            Kind = "Policy",
            Metadata = new PolicyMetadata
            {
                Name = "baseline-governance",
                Namespace = "default",
                Version = "1.0.0",
                CreatedAt = DateTime.UtcNow
            },
            Spec = new PolicySpec
            {
                Mode = "enforce",
                DefaultEffect = "allow",
                Execution = new PolicyExecution
                {
                    Order = "sequential",
                    ShortCircuit = true,
                    ConflictStrategy = "denyOverrides"
                },
                Target = new PolicyTarget
                {
                    ResourceTypes = new List<string> { "Any" },
                    Environments = new List<string> { "dev", "staging", "prod" }
                },
                Rules = new List<PolicyRule>
                {
                    new PolicyRule
                    {
                        Id = "REQUIRE_DATA_CLASSIFICATION",
                        Priority = 10,
                        Description = "Every resource must carry a data classification label.",
                        Enabled = true,
                        Match = new PolicyMatch
                        {
                            Resource = new PolicyResourceMatch { Type = "Any", Name = "*" }
                        },
                        When = new List<PolicyCondition>
                        {
                            new PolicyCondition
                            {
                                Op = "notMatches",
                                Path = "metadata.labels.dataClassification",
                                Value = "^(public|internal|confidential|restricted)$"
                            }
                        },
                        Effect = "deny",
                        Severity = "high",
                        Message = "Missing/invalid metadata.labels.dataClassification. Allowed: public|internal|confidential|restricted.",
                        Remediation = new PolicyRemediation
                        {
                            Hint = "Set metadata.labels.dataClassification to one of the allowed values."
                        }
                    }
                }
            }
        };
    }
}
