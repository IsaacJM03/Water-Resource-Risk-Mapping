import { apiClient } from "./apiClient";

export interface Alert {
  id: number;
  water_source_id: number;
  level: "low" | "medium" | "high" | "critical";
  message: string;
  created_at: string;
  acknowledged: boolean;
}

export async function fetchAlerts(): Promise<Alert[]> {
  return apiClient.get<Alert[]>("/alerts");
}
