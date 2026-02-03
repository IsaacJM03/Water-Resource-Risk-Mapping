
import { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import { fetchSources, WaterSource } from "../../services/sources";
import { Link } from "expo-router";

export default function Dashboard() {
  const [sources, setSources] = useState<WaterSource[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSources()
      .then(setSources)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <Text style={styles.center}>Loading...</Text>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Water Risk Dashboard</Text>

      <FlatList
        data={sources}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <Link href={`/sources/${item.id}`} asChild>
            <View style={styles.card}>
              <Text style={styles.name}>{item.name}</Text>
              <Text>Risk: {item.risk_score}%</Text>
              <Text>Rainfall: {item.rainfall} mm</Text>
              <Text>Water Level: {item.water_level} m</Text>
            </View>
          </Link>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  title: { fontSize: 22, fontWeight: "bold", marginBottom: 12 },
  card: {
    padding: 12,
    marginBottom: 10,
    borderRadius: 8,
    backgroundColor: "#f1f5f9",
  },
  name: { fontSize: 16, fontWeight: "600" },
  center: { marginTop: 40, textAlign: "center" },
});
