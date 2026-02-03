import { View, Text, StyleSheet } from "react-native";
import Card from "./Card";
import { colors, spacing, typography } from "@/constants/theme";

type Props = {
  label: string;
  value: string | number;
  unit?: string;
  icon?: string;
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
};

export default function StatCard({ label, value, unit, icon, trend, trendValue }: Props) {
  const trendColors = {
    up: colors.risk.high,
    down: colors.risk.low,
    neutral: colors.text.secondary,
  };

  const trendIcons = {
    up: "↑",
    down: "↓",
    neutral: "→",
  };

  return (
    <Card style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.label}>{label}</Text>
        {icon && <Text style={styles.icon}>{icon}</Text>}
      </View>
      
      <View style={styles.valueRow}>
        <Text style={styles.value}>
          {value}
          {unit && <Text style={styles.unit}> {unit}</Text>}
        </Text>
      </View>

      {trend && trendValue && (
        <View style={styles.trendRow}>
          <Text style={[styles.trendText, { color: trendColors[trend] }]}>
            {trendIcons[trend]} {trendValue}
          </Text>
          <Text style={styles.trendLabel}>vs last week</Text>
        </View>
      )}
    </Card>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    minWidth: 150,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: spacing.sm,
  },
  label: {
    ...typography.caption,
    color: colors.text.secondary,
  },
  icon: {
    fontSize: 20,
  },
  valueRow: {
    marginBottom: spacing.xs,
  },
  value: {
    ...typography.h2,
    color: colors.text.primary,
  },
  unit: {
    ...typography.body,
    color: colors.text.secondary,
  },
  trendRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
  },
  trendText: {
    ...typography.small,
    fontWeight: "600",
  },
  trendLabel: {
    ...typography.small,
    color: colors.text.light,
  },
});