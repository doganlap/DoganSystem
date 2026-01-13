namespace DoganSystem.Application.Common.Constants
{
    /// <summary>
    /// Centralized error codes following ABP best practices
    /// </summary>
    public static class ErrorCodes
    {
        // General errors
        public const string InternalServerError = "INTERNAL_SERVER_ERROR";
        public const string ValidationError = "VALIDATION_ERROR";
        public const string NotFound = "NOT_FOUND";
        public const string Unauthorized = "UNAUTHORIZED";
        public const string Forbidden = "FORBIDDEN";
        public const string BadRequest = "BAD_REQUEST";

        // Tenant errors
        public const string TenantNotFound = "TENANT_NOT_FOUND";
        public const string TenantSubdomainExists = "TENANT_SUBDOMAIN_EXISTS";
        public const string TenantDomainExists = "TENANT_DOMAIN_EXISTS";
        public const string TenantInactive = "TENANT_INACTIVE";
        public const string TenantSuspended = "TENANT_SUSPENDED";

        // ERPNext errors
        public const string ErpNextInstanceNotFound = "ERPNEXT_INSTANCE_NOT_FOUND";
        public const string ErpNextConnectionFailed = "ERPNEXT_CONNECTION_FAILED";
        public const string ErpNextInvalidCredentials = "ERPNEXT_INVALID_CREDENTIALS";

        // Agent errors
        public const string AgentNotFound = "AGENT_NOT_FOUND";
        public const string AgentInactive = "AGENT_INACTIVE";
        public const string AgentOrchestrationFailed = "AGENT_ORCHESTRATION_FAILED";

        // Subscription errors
        public const string SubscriptionNotFound = "SUBSCRIPTION_NOT_FOUND";
        public const string SubscriptionExpired = "SUBSCRIPTION_EXPIRED";
        public const string SubscriptionCancelled = "SUBSCRIPTION_CANCELLED";
        public const string SubscriptionLimitExceeded = "SUBSCRIPTION_LIMIT_EXCEEDED";

        // Email errors
        public const string EmailSendFailed = "EMAIL_SEND_FAILED";
        public const string EmailConfigurationInvalid = "EMAIL_CONFIGURATION_INVALID";
        public const string EmailServiceUnavailable = "EMAIL_SERVICE_UNAVAILABLE";

        // Policy errors
        public const string PolicyViolation = "POLICY_VIOLATION";
        public const string PolicyEvaluationFailed = "POLICY_EVALUATION_FAILED";
    }
}
