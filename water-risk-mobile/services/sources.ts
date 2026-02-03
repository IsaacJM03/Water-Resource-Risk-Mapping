import { apiClient } from "./apiClient";

/** Backend water source shape */
export interface WaterSource {
  id: number;
  name: string;
  rainfall: number;
  water_level: number;
  latitude: number;
  longitude: number;
  risk_score: number;
  updated_at: string;
  last_updated: string;
}

/** Fetch all water sources */
export async function fetchSources(): Promise<WaterSource[]> {
  return apiClient.get<WaterSource[]>("/sources");
}

/** Fetch one water source */
export async function fetchSourceById(id: number): Promise<WaterSource> {
  return apiClient.get<WaterSource>(`/sources/${id}`);
}

export async function fetchForecast(id: number): Promise<number> {
  const res = await apiClient.get<{ forecast_risk: number }>(
    `/sources/${id}/forecast`
  );
  return res.forecast_risk;
}
