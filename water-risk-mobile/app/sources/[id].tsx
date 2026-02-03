import { useEffect, useState } from "react";
import { View, Text, StyleSheet } from "react-native";
import { useLocalSearchParams } from "expo-router";
import { fetchForecast, fetchSourceById, WaterSource } from "../../services/sources";
import RiskBadge from "../../components/RiskBadge";
import { useAuth } from "../../context/AuthContext";


function formatDate(input: unknown) {
  if (!input) return "—";
  const d = input instanceof Date ? input : new Date(String(input));
  return Number.isNaN(d.getTime()) ? "—" : d.toLocaleString();
}

export default function SourceDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { role } = useAuth();
  const [forecast, setForecast] = useState<number | null>(null);
  const [source, setSource] = useState<WaterSource | null>(null);

  useEffect(() => {
    if (!id) return;

    fetchSourceById(Number(id))
      .then(setSource)
      .catch(console.error);

    fetchForecast(Number(id)).then(setForecast);

  }, [id]);

  if (!source) {
    return <Text style={styles.center}>Loading source...</Text>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{source.name}</Text>
      <RiskBadge risk={source.risk_score} />
      <Text>Risk Score: {source.risk_score}%</Text>
      <Text>Rainfall: {source.rainfall} mm</Text>
      <Text>Water Level: {source.water_level} m</Text>
      {forecast && (
        <Text style={{ marginTop: 10 }}>
          Forecasted Risk: {forecast}%
        </Text>
      )}


      <Text style={styles.meta}>
        Last updated: {formatDate(source?.last_updated)}
      </Text>

      {role === "admin" && (
        <Text style={{ marginTop: 12, color: "red" }}>
          Admin actions enabled
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  title: { fontSize: 22, fontWeight: "bold", marginBottom: 12 },
  meta: { marginTop: 10, color: "#555" },
  center: { marginTop: 40, textAlign: "center" },
});
