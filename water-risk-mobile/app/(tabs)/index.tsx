import { View, Text, FlatList, StyleSheet, TouchableOpacity, RefreshControl } from "react-native";
import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { fetchSources } from "@/services/sources";
import { connectRealtime, disconnectRealtime } from "@/services/realtime";
import type { WaterSource } from "@/services/sources";
import RiskBadge from "@/components/RiskBadge";
import Card from "@/components/Card";
import StatCard from "@/components/StatCard";
import { colors, spacing, typography, borderRadius } from "@/constants/theme";

export default function Dashboard() {
  const router = useRouter();
  const [sources, setSources] = useState<WaterSource[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async () => {
    try {
      const data = await fetchSources();
      setSources(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();

    connectRealtime((payload) => {
      if (payload.type === "risk_update") {
        setSources((prev) =>
          prev.map((s) => (s.id === payload.source_id ? payload.data : s))
        );
      }
    });

    return () => disconnectRealtime();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  // Calculate stats
  const avgRisk = sources.length
    ? Math.round(sources.reduce((sum, s) => sum + (s.risk_score ?? 0), 0) / sources.length)
    : 0;
  const highRiskCount = sources.filter((s) => (s.risk_score ?? 0) >= 50).length;
  const activeAlerts = sources.filter((s) => (s.risk_score ?? 0) >= 70).length;

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Water Risk Dashboard</Text>
        <Text style={styles.subtitle}>Real-time monitoring & analytics</Text>
      </View>

      {/* Stats Overview */}
      <View style={styles.statsGrid}>
        <StatCard
          label="Sources"
          value={sources.length}
          icon="💧"
          trend="up"
          trendValue="+2"
        />
        <StatCard
          label="Avg Risk"
          value={avgRisk}
          unit="%"
          icon="📊"
          trend={avgRisk > 50 ? "up" : "down"}
          trendValue={`${avgRisk}%`}
        />
      </View>

      <View style={styles.statsGrid}>
        <StatCard
          label="High Risk"
          value={highRiskCount}
          icon="⚠️"
          trend="neutral"
          trendValue="0"
        />
        <StatCard
          label="Active Alerts"
          value={activeAlerts}
          icon="🔔"
          trend={activeAlerts > 0 ? "up" : "neutral"}
          trendValue={`${activeAlerts}`}
        />
      </View>

      {/* Sources List */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Water Sources</Text>
        <FlatList
          data={sources}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <TouchableOpacity
              onPress={() => router.push(`/sources/${item.id}`)}
              activeOpacity={0.7}
            >
              <Card style={styles.sourceCard}>
                <View style={styles.sourceHeader}>
                  <View style={styles.sourceInfo}>
                    <Text style={styles.sourceName}>{item.name}</Text>
                    <Text style={styles.sourceLocation}>
                      📍 {item.latitude.toFixed(2)}, {item.longitude.toFixed(2)}
                    </Text>
                  </View>
                  <RiskBadge risk={item.risk_score} size="small" showLabel={false} />
                </View>

                <View style={styles.sourceMetrics}>
                  <View style={styles.metric}>
                    <Text style={styles.metricLabel}>💧 Water Level</Text>
                    <Text style={styles.metricValue}>{item.water_level ?? "—"} m</Text>
                  </View>
                  <View style={styles.metric}>
                    <Text style={styles.metricLabel}>🌧️ Rainfall</Text>
                    <Text style={styles.metricValue}>{item.rainfall ?? "—"} mm</Text>
                  </View>
                </View>
              </Card>
            </TouchableOpacity>
          )}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          contentContainerStyle={styles.listContent}
          showsVerticalScrollIndicator={false}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    padding: spacing.lg,
    backgroundColor: colors.primary,
    paddingTop: spacing.xl,
  },
  title: {
    ...typography.h1,
    color: colors.surface,
  },
  subtitle: {
    ...typography.body,
    color: colors.surface,
    opacity: 0.9,
    marginTop: spacing.xs,
  },
  statsGrid: {
    flexDirection: "row",
    gap: spacing.md,
    paddingHorizontal: spacing.md,
    marginTop: spacing.md,
  },
  section: {
    flex: 1,
    marginTop: spacing.lg,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.text.primary,
    paddingHorizontal: spacing.lg,
    marginBottom: spacing.md,
  },
  listContent: {
    paddingHorizontal: spacing.md,
    paddingBottom: spacing.xl,
  },
  sourceCard: {
    marginBottom: spacing.md,
  },
  sourceHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: spacing.md,
  },
  sourceInfo: {
    flex: 1,
  },
  sourceName: {
    ...typography.h3,
    color: colors.text.primary,
    marginBottom: spacing.xs,
  },
  sourceLocation: {
    ...typography.caption,
    color: colors.text.secondary,
  },
  sourceMetrics: {
    flexDirection: "row",
    gap: spacing.lg,
    paddingTop: spacing.sm,
    borderTopWidth: 1,
    borderTopColor: colors.border,
  },
  metric: {
    flex: 1,
  },
  metricLabel: {
    ...typography.small,
    color: colors.text.secondary,
    marginBottom: spacing.xs,
  },
  metricValue: {
    ...typography.body,
    color: colors.text.primary,
    fontWeight: "600",
  },
});
