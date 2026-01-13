/**
 * API Service - Centralized API client for DoganSystem
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://localhost:5001';
const PYTHON_API_URL = process.env.NEXT_PUBLIC_PYTHON_API_URL || 'http://localhost:8007';

// Token storage keys
const TOKEN_KEY = 'doganSystem_token';
const REFRESH_TOKEN_KEY = 'doganSystem_refreshToken';
const USER_KEY = 'doganSystem_user';
const TWO_FACTOR_SESSION_KEY = 'doganSystem_2faSession';

// Types
export interface LoginRequest {
  userNameOrEmail: string;
  password: string;
  rememberMe?: boolean;
  twoFactorCode?: string;
}

export interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
  expiresIn: number;
  userId: string;
  userName: string;
  email: string;
  name: string;
  roles: string[];
  requiresTwoFactor?: boolean;
  twoFactorSessionToken?: string;
}

export interface User {
  userId: string;
  userName: string;
  email: string;
  name: string;
  roles?: string[];
}

export interface ApiError {
  error: string;
  details?: string;
}

export interface TwoFactorSetupResponse {
  secretKey: string;
  qrCodeUri: string;
  backupCodes: string[];
}

export interface TwoFactorStatusResponse {
  isEnabled: boolean;
  hasBackupCodes: boolean;
}

export interface SessionInfo {
  sessionId: string;
  deviceInfo: string;
  ipAddress: string;
  createdAt: string;
  lastActivity: string;
  isCurrent: boolean;
}

export interface RefreshTokenRequest {
  refreshToken: string;
}

export interface RefreshTokenResponse {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

// Token management
export const getToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
};

export const setToken = (token: string): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(TOKEN_KEY, token);
};

export const getRefreshToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

export const setRefreshToken = (token: string): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(REFRESH_TOKEN_KEY, token);
};

export const get2FASessionToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TWO_FACTOR_SESSION_KEY);
};

export const set2FASessionToken = (token: string): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(TWO_FACTOR_SESSION_KEY, token);
};

export const removeToken = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem(TWO_FACTOR_SESSION_KEY);
};

export const getStoredUser = (): User | null => {
  if (typeof window === 'undefined') return null;
  const user = localStorage.getItem(USER_KEY);
  return user ? JSON.parse(user) : null;
};

export const setStoredUser = (user: User): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  return !!getToken();
};

// API fetch wrapper with authentication
async function apiFetch<T>(
  url: string,
  options: RequestInit = {},
  useAuth: boolean = true
): Promise<T> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (useAuth) {
    const token = getToken();
    if (token) {
      (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
    }
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // Handle token expiration
  if (response.status === 401) {
    const tokenExpired = response.headers.get('Token-Expired');
    if (tokenExpired === 'true') {
      removeToken();
      window.location.href = '/login?expired=true';
      throw new Error('Token expired');
    }
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(errorData.error || `HTTP ${response.status}`);
  }

  return response.json();
}

// Auth API
export const authApi = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await apiFetch<LoginResponse>(
      `${API_BASE_URL}/api/auth/login`,
      {
        method: 'POST',
        body: JSON.stringify(credentials),
      },
      false // No auth needed for login
    );

    // Check if 2FA is required
    if (response.requiresTwoFactor && response.twoFactorSessionToken) {
      set2FASessionToken(response.twoFactorSessionToken);
      return response;
    }

    // Store tokens and user
    setToken(response.accessToken);
    if (response.refreshToken) {
      setRefreshToken(response.refreshToken);
    }
    setStoredUser({
      userId: response.userId,
      userName: response.userName,
      email: response.email,
      name: response.name,
      roles: response.roles,
    });

    return response;
  },

  completeTwoFactorLogin: async (code: string): Promise<LoginResponse> => {
    const sessionToken = get2FASessionToken();
    if (!sessionToken) {
      throw new Error('No 2FA session found');
    }

    const response = await apiFetch<LoginResponse>(
      `${API_BASE_URL}/api/auth/login/2fa`,
      {
        method: 'POST',
        body: JSON.stringify({ sessionToken, code }),
      },
      false
    );

    // Store tokens and user
    setToken(response.accessToken);
    if (response.refreshToken) {
      setRefreshToken(response.refreshToken);
    }
    setStoredUser({
      userId: response.userId,
      userName: response.userName,
      email: response.email,
      name: response.name,
      roles: response.roles,
    });

    // Clear 2FA session
    localStorage.removeItem(TWO_FACTOR_SESSION_KEY);

    return response;
  },

  logout: async (): Promise<void> => {
    try {
      await apiFetch(`${API_BASE_URL}/api/auth/logout`, {
        method: 'POST',
      });
    } catch {
      // Ignore logout errors
    }
    removeToken();
    window.location.href = '/login';
  },

  getCurrentUser: async (): Promise<User> => {
    return apiFetch<User>(`${API_BASE_URL}/api/auth/me`);
  },

  changePassword: async (currentPassword: string, newPassword: string): Promise<void> => {
    await apiFetch(`${API_BASE_URL}/api/auth/change-password`, {
      method: 'POST',
      body: JSON.stringify({ currentPassword, newPassword }),
    });
  },

  // Refresh token
  refreshToken: async (): Promise<RefreshTokenResponse> => {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiFetch<RefreshTokenResponse>(
      `${API_BASE_URL}/api/auth/refresh-token`,
      {
        method: 'POST',
        body: JSON.stringify({ refreshToken }),
      },
      false
    );

    setToken(response.accessToken);
    setRefreshToken(response.refreshToken);
    return response;
  },

  // Password Reset
  forgotPassword: async (email: string): Promise<{ message: string }> => {
    return apiFetch<{ message: string }>(
      `${API_BASE_URL}/api/auth/forgot-password`,
      {
        method: 'POST',
        body: JSON.stringify({ email }),
      },
      false
    );
  },

  resetPassword: async (email: string, token: string, newPassword: string): Promise<{ message: string }> => {
    return apiFetch<{ message: string }>(
      `${API_BASE_URL}/api/auth/reset-password`,
      {
        method: 'POST',
        body: JSON.stringify({ email, token, newPassword }),
      },
      false
    );
  },

  // Two-Factor Authentication
  twoFactor: {
    getStatus: async (): Promise<TwoFactorStatusResponse> => {
      return apiFetch<TwoFactorStatusResponse>(`${API_BASE_URL}/api/auth/2fa/status`);
    },

    setup: async (): Promise<TwoFactorSetupResponse> => {
      return apiFetch<TwoFactorSetupResponse>(`${API_BASE_URL}/api/auth/2fa/setup`, {
        method: 'POST',
      });
    },

    verifySetup: async (code: string): Promise<{ message: string; backupCodes: string[] }> => {
      return apiFetch<{ message: string; backupCodes: string[] }>(
        `${API_BASE_URL}/api/auth/2fa/verify-setup`,
        {
          method: 'POST',
          body: JSON.stringify({ code }),
        }
      );
    },

    disable: async (password: string): Promise<{ message: string }> => {
      return apiFetch<{ message: string }>(
        `${API_BASE_URL}/api/auth/2fa/disable`,
        {
          method: 'POST',
          body: JSON.stringify({ password }),
        }
      );
    },

    regenerateBackupCodes: async (password: string): Promise<{ backupCodes: string[] }> => {
      return apiFetch<{ backupCodes: string[] }>(
        `${API_BASE_URL}/api/auth/2fa/backup-codes`,
        {
          method: 'POST',
          body: JSON.stringify({ password }),
        }
      );
    },
  },

  // Session Management
  sessions: {
    getAll: async (): Promise<SessionInfo[]> => {
      return apiFetch<SessionInfo[]>(`${API_BASE_URL}/api/auth/sessions`);
    },

    revoke: async (sessionId: string): Promise<{ message: string }> => {
      return apiFetch<{ message: string }>(
        `${API_BASE_URL}/api/auth/sessions/${sessionId}`,
        {
          method: 'DELETE',
        }
      );
    },

    revokeAll: async (): Promise<{ message: string }> => {
      return apiFetch<{ message: string }>(
        `${API_BASE_URL}/api/auth/sessions`,
        {
          method: 'DELETE',
        }
      );
    },
  },
};

// Tenants API
export const tenantsApi = {
  getList: async (params?: { filter?: string; status?: string; skip?: number; take?: number }) => {
    const query = new URLSearchParams();
    if (params?.filter) query.set('filter', params.filter);
    if (params?.status) query.set('status', params.status);
    if (params?.skip) query.set('skipCount', params.skip.toString());
    if (params?.take) query.set('maxResultCount', params.take.toString());

    return apiFetch(`${API_BASE_URL}/api/tenants?${query}`);
  },

  get: async (id: string) => {
    return apiFetch(`${API_BASE_URL}/api/tenants/${id}`);
  },

  create: async (data: any) => {
    return apiFetch(`${API_BASE_URL}/api/tenants`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  update: async (id: string, data: any) => {
    return apiFetch(`${API_BASE_URL}/api/tenants/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  delete: async (id: string) => {
    return apiFetch(`${API_BASE_URL}/api/tenants/${id}`, {
      method: 'DELETE',
    });
  },
};

// ERPNext API
export const erpNextApi = {
  getList: async () => {
    return apiFetch(`${API_BASE_URL}/api/erpnext`);
  },

  get: async (id: string) => {
    return apiFetch(`${API_BASE_URL}/api/erpnext/${id}`);
  },

  create: async (data: any) => {
    return apiFetch(`${API_BASE_URL}/api/erpnext`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  testConnection: async (id: string) => {
    return apiFetch(`${API_BASE_URL}/api/erpnext/${id}/test-connection`, {
      method: 'POST',
    });
  },
};

// Agents API
export const agentsApi = {
  getList: async (params?: { tenantId?: string; department?: string; status?: string }) => {
    const query = new URLSearchParams();
    if (params?.tenantId) query.set('tenantId', params.tenantId);
    if (params?.department) query.set('department', params.department);
    if (params?.status) query.set('status', params.status);

    return apiFetch(`${API_BASE_URL}/api/agents?${query}`);
  },

  get: async (id: string) => {
    return apiFetch(`${API_BASE_URL}/api/agents/${id}`);
  },

  create: async (data: any) => {
    return apiFetch(`${API_BASE_URL}/api/agents`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

// Consultant Offers API
export const offersApi = {
  getList: async (params?: { status?: string; employeeAgentId?: string; skip?: number; take?: number }) => {
    const query = new URLSearchParams();
    if (params?.status) query.set('status', params.status);
    if (params?.employeeAgentId) query.set('employeeAgentId', params.employeeAgentId);
    if (params?.skip) query.set('skipCount', params.skip.toString());
    if (params?.take) query.set('maxResultCount', params.take.toString());

    return apiFetch(`${API_BASE_URL}/api/consultant-offers?${query}`);
  },

  get: async (id: string) => {
    return apiFetch(`${API_BASE_URL}/api/consultant-offers/${id}`);
  },

  create: async (data: any) => {
    return apiFetch(`${API_BASE_URL}/api/consultant-offers`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  update: async (id: string, data: any) => {
    return apiFetch(`${API_BASE_URL}/api/consultant-offers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  send: async (id: string) => {
    return apiFetch(`${API_BASE_URL}/api/consultant-offers/${id}/send`, {
      method: 'POST',
    });
  },

  accept: async (id: string) => {
    return apiFetch(`${API_BASE_URL}/api/consultant-offers/${id}/accept`, {
      method: 'POST',
    });
  },

  reject: async (id: string, reason?: string) => {
    return apiFetch(`${API_BASE_URL}/api/consultant-offers/${id}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
    });
  },
};

// Python Dashboard API (for AI employees & workflows)
export const dashboardApi = {
  getStats: async () => {
    return apiFetch(`${PYTHON_API_URL}/api/dashboard/stats`, {}, false);
  },

  getEmployees: async (params?: { department?: string; status?: string }) => {
    const query = new URLSearchParams();
    if (params?.department) query.set('department', params.department);
    if (params?.status) query.set('status', params.status);

    return apiFetch(`${PYTHON_API_URL}/api/employees?${query}`, {}, false);
  },

  getEmployee: async (id: string) => {
    return apiFetch(`${PYTHON_API_URL}/api/employees/${id}`, {}, false);
  },

  getWorkflows: async () => {
    return apiFetch(`${PYTHON_API_URL}/api/workflows`, {}, false);
  },

  executeWorkflow: async (id: string) => {
    return apiFetch(`${PYTHON_API_URL}/api/workflows/${id}/execute`, {
      method: 'POST',
    }, false);
  },

  getTasks: async (params?: { employeeId?: string; status?: string; limit?: number }) => {
    const query = new URLSearchParams();
    if (params?.employeeId) query.set('employee_id', params.employeeId);
    if (params?.status) query.set('status', params.status);
    if (params?.limit) query.set('limit', params.limit.toString());

    return apiFetch(`${PYTHON_API_URL}/api/tasks?${query}`, {}, false);
  },

  getActiveTasks: async () => {
    return apiFetch(`${PYTHON_API_URL}/api/tasks/active`, {}, false);
  },

  getOrgChart: async () => {
    return apiFetch(`${PYTHON_API_URL}/api/org-chart`, {}, false);
  },

  getDepartments: async () => {
    return apiFetch(`${PYTHON_API_URL}/api/departments`, {}, false);
  },

  getPerformanceAnalytics: async () => {
    return apiFetch(`${PYTHON_API_URL}/api/analytics/performance`, {}, false);
  },

  healthCheck: async () => {
    return apiFetch(`${PYTHON_API_URL}/api/health`, {}, false);
  },
};

export default {
  auth: authApi,
  tenants: tenantsApi,
  erpNext: erpNextApi,
  agents: agentsApi,
  offers: offersApi,
  dashboard: dashboardApi,
};
