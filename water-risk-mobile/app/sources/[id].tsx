import {
  View,
  Text,
  ScrollView,
  ActivityIndicator,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useEffect, useState } from "react";
import RiskBadge from "@/components/RiskBadge";
import Card from "@/components/Card";
import StatCard from "@/components/StatCard";
import { fetchSourceById } from "@/services/sources";
import type { WaterSource } from "@/services/sources";
import { useAuth } from "@/context/AuthContext";
import { colors, spacing, typography, borderRadius } from "@/constants/theme";

function formatDate(input: unknown) {
  if (!input) return "—";
  const d = input instanceof Date ? input : new Date(String(input));
  return Number.isNaN(d.getTime()) ? "—" : d.toLocaleString();
}

export default function SourceDetail() {
  const { id } = useLocalSearchParams();
  const router = useRouter();
  const { role } = useAuth();
  const [source, setSource] = useState<WaterSource | null>(null);
  const [forecast, setForecast] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    const sourceId = Number(id);

    fetchSourceById(sourceId)
      .then(setSource)
      .catch(console.error)
      .finally(() => setLoading(false));

    fetch(`http://localhost:8000/analytics/forecast/${sourceId}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data?.forecast) setForecast(data.forecast);
      })
      .catch((err) => console.warn("Forecast fetch failed:", err));
  }, [id]);

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  if (!source) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>❌ Source not found</Text>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => router.back()}
        >
          <Text style={styles.backButtonText}>← Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <Card style={styles.headerCard}>
        <Text style={styles.sourceName}>{source.name}</Text>
        <Text style={styles.location}>
          📍 {source.latitude.toFixed(4)}, {source.longitude.toFixed(4)}
        </Text>
        <View style={styles.riskBadgeContainer}>
          <RiskBadge risk={source.risk_score} size="large" />
        </View>
      </Card>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Current Conditions</Text>
        <View style={styles.metricsGrid}>
          <StatCard
            label="Water Level"
            value={source.water_level ?? "—"}
            unit="m"
            icon="💧"
          />
          <StatCard
            label="Rainfall"
            value={source.rainfall ?? "—"}
            unit="mm"
            icon="🌧️"
          />
        </View>
      </View>

      {forecast !== null && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>7-Day Forecast</Text>
          <Card>
            <View style={styles.forecastContainer}>
              <Text style={styles.forecastLabel}>Predicted Risk</Text>
              <Text style={styles.forecastValue}>{forecast}%</Text>
              <RiskBadge risk={forecast} size="medium" />
            </View>
          </Card>
        </View>
      )}

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Details</Text>
        <Card>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Organization ID</Text>
            <Text style={styles.detailValue}>{source.organization_id}</Text>
          </View>
          <View style={[styles.detailRow, styles.detailRowLast]}>
            <Text style={styles.detailLabel}>Last Updated</Text>
            <Text style={styles.detailValue}>
              {formatDate(source?.last_updated)}
            </Text>
          </View>
        </Card>
      </View>

      {role === "admin" && (
        <View style={styles.section}>
          <Card style={styles.adminCard}>
            <Text style={styles.adminTitle}>🔐 Admin Actions</Text>
            <TouchableOpacity style={styles.adminButton}>
              <Text style={styles.adminButtonText}>Update Source Data</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.adminButton}>
              <Text style={styles.adminButtonText}>View History</Text>
            </TouchableOpacity>
          </Card>
        </View>
      )}

      <View style={{ height: spacing.xl }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  centerContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: colors.background,
  },
  headerCard: {
    margin: spacing.md,
    marginTop: spacing.lg,
  },
  sourceName: {
    ...typography.h1,
    color: colors.text.primary,
    marginBottom: spacing.xs,
  },
  location: {
    ...typography.body,
    color: colors.text.secondary,
    marginBottom: spacing.md,
  },
  riskBadgeContainer: {
    marginTop: spacing.sm,
  },
  section: {
    marginTop: spacing.lg,
    paddingHorizontal: spacing.md,
  },
  sectionTitle: {
    ...typography.h3,
    color: colors.text.primary,
    marginBottom: spacing.md,
  },
  metricsGrid: {
    flexDirection: "row",
    gap: spacing.md,
  },
  forecastContainer: {
    alignItems: "center",
    paddingVertical: spacing.md,
  },
  forecastLabel: {
    ...typography.caption,
    color: colors.text.secondary,
    marginBottom: spacing.xs,
  },
  forecastValue: {
    ...typography.h1,
    color: colors.text.primary,
    marginBottom: spacing.md,
  },
  detailRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  detailRowLast: {
    borderBottomWidth: 0,
  },
  detailLabel: {
    ...typography.body,
    color: colors.text.secondary,
  },
  detailValue: {
    ...typography.body,
    color: colors.text.primary,
    fontWeight: "600",
  },
  adminCard: {
    backgroundColor: `${colors.secondary}10`,
    borderWidth: 1,
    borderColor: colors.secondary,
  },
  adminTitle: {
    ...typography.h3,
    color: colors.secondary,
    marginBottom: spacing.md,
  },
  adminButton: {
    backgroundColor: colors.secondary,
    padding: spacing.md,
    borderRadius: borderRadius.md,
    marginTop: spacing.sm,
  },
  adminButtonText: {
    ...typography.body,
    color: colors.surface,
    textAlign: "center",
    fontWeight: "600",
  },
  errorText: {
    ...typography.h2,
    color: colors.text.secondary,
    marginBottom: spacing.lg,
  },
  backButton: {
    backgroundColor: colors.primary,
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.md,
  },
  backButtonText: {
    ...typography.body,
    color: colors.surface,
    fontWeight: "600",
  },
});
