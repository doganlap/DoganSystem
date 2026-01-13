using Volo.Abp;
using DoganSystem.Application.Common.Constants;

namespace DoganSystem.Application.Common.Exceptions
{
    /// <summary>
    /// Extension methods for BusinessException following ABP best practices
    /// </summary>
    public static class BusinessExceptionExtensions
    {
        public static BusinessException TenantNotFound(Guid tenantId)
        {
            return new BusinessException(ErrorCodes.TenantNotFound, $"Tenant with ID '{tenantId}' was not found.");
        }

        public static BusinessException TenantSubdomainExists(string subdomain)
        {
            return new BusinessException(ErrorCodes.TenantSubdomainExists, $"Subdomain '{subdomain}' is already taken.");
        }

        public static BusinessException TenantInactive(Guid tenantId)
        {
            return new BusinessException(ErrorCodes.TenantInactive, $"Tenant with ID '{tenantId}' is not active.");
        }

        public static BusinessException ErpNextConnectionFailed(string instanceUrl)
        {
            return new BusinessException(ErrorCodes.ErpNextConnectionFailed, $"Failed to connect to ERPNext instance at '{instanceUrl}'.");
        }

        public static BusinessException AgentNotFound(Guid agentId)
        {
            return new BusinessException(ErrorCodes.AgentNotFound, $"Agent with ID '{agentId}' was not found.");
        }

        public static BusinessException SubscriptionExpired(Guid subscriptionId)
        {
            return new BusinessException(ErrorCodes.SubscriptionExpired, $"Subscription with ID '{subscriptionId}' has expired.");
        }

        public static BusinessException EmailSendFailed(string recipient)
        {
            return new BusinessException(ErrorCodes.EmailSendFailed, $"Failed to send email to '{recipient}'.");
        }
    }
}
