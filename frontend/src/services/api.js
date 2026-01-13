import axios from 'axios';

// API Base URL - Can be configured via environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8006/api';

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
  getAll: (params) => apiClient.get('/tenants', { params }),
  getById: (id) => apiClient.get(`/tenants/${id}`),
  create: (data) => apiClient.post('/tenants', data),
  update: (id, data) => apiClient.put(`/tenants/${id}`, data),
  delete: (id) => apiClient.delete(`/tenants/${id}`),
  getDashboard: (tenantId) => apiClient.get(`/tenants/${tenantId}/dashboard`),
  getMetrics: (tenantId) => apiClient.get(`/tenants/${tenantId}/metrics`),
  getUsage: (tenantId) => apiClient.get(`/tenants/${tenantId}/usage`),
};

// Agent API
export const agentApi = {
  getAll: (params) => apiClient.get('/agents', { params }),
  getById: (agentId) => apiClient.get(`/agents/${agentId}`),
  create: (data) => apiClient.post('/agents', data),
  update: (agentId, data) => apiClient.put(`/agents/${agentId}`, data),
  delete: (agentId) => apiClient.delete(`/agents/${agentId}`),
};

// ERPNext API
export const erpNextApi = {
  getAll: (params) => apiClient.get('/erpnext', { params }),
  getById: (instanceId) => apiClient.get(`/erpnext/${instanceId}`),
  create: (data) => apiClient.post('/erpnext', data),
  update: (instanceId, data) => apiClient.put(`/erpnext/${instanceId}`, data),
  delete: (instanceId) => apiClient.delete(`/erpnext/${instanceId}`),
  testConnection: (instanceId) => apiClient.post(`/erpnext/${instanceId}/test-connection`),
};

// Subscription API
export const subscriptionApi = {
  getAll: (params) => apiClient.get('/subscriptions', { params }),
  create: (data) => apiClient.post('/subscriptions', data),
  cancel: (subscriptionId) => apiClient.post(`/subscriptions/${subscriptionId}/cancel`),
  getInvoices: () => apiClient.get('/subscriptions/invoices'),
};

// Module API
export const moduleApi = {
  getAll: () => apiClient.get('/modules'),
  purchase: (moduleId, data) => apiClient.post(`/modules/${moduleId}/purchase`, data),
};

export default apiClient;
