import axios from 'axios';

// API Base URL - Can be configured via environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8006/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// System API
export const systemApi = {
  getStatus: () => apiClient.get('/system/status'),
};

// Tenant API
export const tenantApi = {
  getAll: (params) => apiClient.get('/admin/tenants', { params }),
  getById: (id) => apiClient.get(`/admin/tenants/${id}`),
  create: (data) => apiClient.post('/admin/tenants', data),
  update: (id, data) => apiClient.put(`/admin/tenants/${id}`, data),
  delete: (id) => apiClient.delete(`/admin/tenants/${id}`),
  getDashboard: (tenantId) => apiClient.get(`/${tenantId}/admin/dashboard`),
  getMetrics: (tenantId) => apiClient.get(`/${tenantId}/admin/metrics`),
  getUsage: (tenantId) => apiClient.get(`/${tenantId}/admin/usage`),
};

// Agent API
export const agentApi = {
  getAll: (tenantId, params) => apiClient.get(`/${tenantId}/agents`, { params }),
  getById: (tenantId, agentId) => apiClient.get(`/${tenantId}/agents/${agentId}`),
  create: (tenantId, data) => apiClient.post(`/${tenantId}/agents`, data),
  update: (tenantId, agentId, data) => apiClient.put(`/${tenantId}/agents/${agentId}`, data),
  delete: (tenantId, agentId) => apiClient.delete(`/${tenantId}/agents/${agentId}`),
};

// ERPNext API
export const erpNextApi = {
  getAll: (tenantId, params) => apiClient.get(`/${tenantId}/erpnext`, { params }),
  getById: (tenantId, instanceId) => apiClient.get(`/${tenantId}/erpnext/${instanceId}`),
  create: (tenantId, data) => apiClient.post(`/${tenantId}/erpnext`, data),
  update: (tenantId, instanceId, data) => apiClient.put(`/${tenantId}/erpnext/${instanceId}`, data),
  delete: (tenantId, instanceId) => apiClient.delete(`/${tenantId}/erpnext/${instanceId}`),
  testConnection: (tenantId, instanceId) => apiClient.post(`/${tenantId}/erpnext/${instanceId}/test-connection`),
};

// Subscription API
export const subscriptionApi = {
  getAll: (tenantId, params) => apiClient.get(`/${tenantId}/billing/subscriptions`, { params }),
  create: (tenantId, data) => apiClient.post(`/${tenantId}/billing/subscription`, data),
  cancel: (tenantId, subscriptionId) => apiClient.post(`/${tenantId}/billing/subscriptions/${subscriptionId}/cancel`),
  getInvoices: (tenantId) => apiClient.get(`/${tenantId}/billing/invoices`),
};

// Module API
export const moduleApi = {
  getAll: (tenantId) => apiClient.get(`/${tenantId}/modules`),
  purchase: (tenantId, moduleId, data) => apiClient.post(`/${tenantId}/modules/${moduleId}/purchase`, data),
};

export default apiClient;
