const API_BASE_URL = "http://localhost:8000"; 
// later → env / deployed URL

type RequestOptions = RequestInit & {
  auth?: boolean;
};

// Type definitions matching backend schemas
export interface WaterSource {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  rainfall: number;
  water_level: number;
  organization_id: number;
  risk_score?: number;
  created_at: string;
  last_updated?: string;
}

export interface Alert {
  id: number;
  water_source_id: number;
  level: string;
  message: string;
  acknowledged: boolean;
  organization_id?: number;
  created_at: string;
}

export interface RiskHistory {
  id: number;
  water_source_id: number;
  risk_score: number;
  timestamp: string;
}

async function request<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  // auth hook (future)
  if (options.auth) {
    // const token = await getToken()
    // headers.Authorization = `Bearer ${token}`
  }

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || "API error");
  }

  return res.json();
}

export const apiClient = {
  get: <T>(endpoint: string) =>
    request<T>(endpoint, { method: "GET" }),

  post: <T>(endpoint: string, body?: unknown) =>
    request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    }),

  put: <T>(endpoint: string, body?: unknown) =>
    request<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
    }),

  delete: <T>(endpoint: string) =>
    request<T>(endpoint, { method: "DELETE" }),
};

// Water Sources API
export const waterSourcesApi = {
  getAll: () => apiClient.get<WaterSource[]>('/sources'),
  getById: (id: number) => apiClient.get<WaterSource>(`/sources/${id}`),
  getRiskHistory: (id: number) => apiClient.get<RiskHistory[]>(`/sources/${id}/risk-history`),
};

// Alerts API
export const alertsApi = {
  getAll: () => apiClient.get<Alert[]>('/alerts'),
  getUnacknowledged: () => apiClient.get<Alert[]>('/alerts/unacknowledged'),
  acknowledge: (id: number) => apiClient.post(`/alerts/${id}/acknowledge`),
};

// Analytics API
export const analyticsApi = {
  getTrends: (sourceId: number, days: number = 30) => 
    apiClient.get(`/analytics/trends/${sourceId}?days=${days}`),
  getForecast: (sourceId: number) => 
    apiClient.get(`/analytics/forecast/${sourceId}`),
  getDashboardStats: () => apiClient.get('/dashboard'),
};
