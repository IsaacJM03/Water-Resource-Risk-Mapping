import { useEffect, useState } from "react";
import { View, Text, StyleSheet } from "react-native";
import { useLocalSearchParams } from "expo-router";
import { fetchSourceById, WaterSource } from "../../services/sources";

export default function SourceDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [source, setSource] = useState<WaterSource | null>(null);

  useEffect(() => {
    if (!id) return;

    fetchSourceById(Number(id))
      .then(setSource)
      .catch(console.error);
  }, [id]);

  if (!source) {
    return <Text style={styles.center}>Loading source...</Text>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{source.name}</Text>

      <Text>Risk Score: {source.risk_score}%</Text>
      <Text>Rainfall: {source.rainfall} mm</Text>
      <Text>Water Level: {source.water_level} m</Text>

      <Text style={styles.meta}>
        Last updated: {new Date(source.updated_at).toLocaleString()}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  title: { fontSize: 22, fontWeight: "bold", marginBottom: 12 },
  meta: { marginTop: 10, color: "#555" },
  center: { marginTop: 40, textAlign: "center" },
});
