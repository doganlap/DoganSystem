import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

/**
 * Custom hook for API queries
 * @param {string} queryKey - Unique key for the query
 * @param {Function} queryFn - Function that returns a promise
 * @param {Object} options - Additional options for useQuery
 */
export const useApiQuery = (queryKey, queryFn, options = {}) => {
  return useQuery({
    queryKey: Array.isArray(queryKey) ? queryKey : [queryKey],
    queryFn,
    ...options,
  });
};

/**
 * Custom hook for API mutations
 * @param {Function} mutationFn - Function that performs the mutation
 * @param {Object} options - Additional options for useMutation
 */
export const useApiMutation = (mutationFn, options = {}) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn,
    onSuccess: (data, variables, context) => {
      // Invalidate and refetch queries after successful mutation
      if (options.invalidateQueries) {
        options.invalidateQueries.forEach((key) => {
          queryClient.invalidateQueries({ queryKey: [key] });
        });
      }

      if (options.onSuccess) {
        options.onSuccess(data, variables, context);
      }
    },
    ...options,
  });
};

// Specific hooks for common operations
export const useTenants = (params) => {
  const { tenantApi } = require('../services/api');
  return useApiQuery('tenants', () => tenantApi.getAll(params));
};

export const useTenant = (id) => {
  const { tenantApi } = require('../services/api');
  return useApiQuery(['tenant', id], () => tenantApi.getById(id), {
    enabled: !!id,
  });
};

export const useAgents = (params) => {
  const { agentApi } = require('../services/api');
  return useApiQuery('agents', () => agentApi.getAll(params));
};

export const useSystemStatus = () => {
  const { systemApi } = require('../services/api');
  return useApiQuery('systemStatus', () => systemApi.getStatus(), {
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};

export const useTenantDashboard = (tenantId) => {
  const { tenantApi } = require('../services/api');
  return useApiQuery(['dashboard', tenantId], () => tenantApi.getDashboard(tenantId), {
    enabled: !!tenantId,
    refetchInterval: 60000, // Refetch every minute
  });
};

export const useTenantMetrics = (tenantId) => {
  const { tenantApi } = require('../services/api');
  return useApiQuery(['metrics', tenantId], () => tenantApi.getMetrics(tenantId), {
    enabled: !!tenantId,
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};
