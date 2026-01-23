import { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import { fetchAlerts, Alert } from "../services/alerts";

export default function AlertsScreen() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    fetchAlerts()
      .then(setAlerts)
      .catch(console.error);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Active Alerts</Text>

      {alerts.length === 0 && (
        <Text style={styles.empty}>No active alerts 🎉</Text>
      )}

      <FlatList
        data={alerts}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.alertCard}>
            <Text style={styles.level}>{item.level.toUpperCase()}</Text>
            <Text>{item.message}</Text>
            <Text style={styles.time}>
              {new Date(item.created_at).toLocaleString()}
            </Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  title: { fontSize: 22, fontWeight: "bold", marginBottom: 12 },
  alertCard: {
    padding: 12,
    marginBottom: 10,
    borderRadius: 8,
    backgroundColor: "#fee2e2",
  },
  level: { fontWeight: "bold", marginBottom: 4 },
  time: { fontSize: 12, color: "#555", marginTop: 4 },
  empty: { marginTop: 40, textAlign: "center", color: "#666" },
});
