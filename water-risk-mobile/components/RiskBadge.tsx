import { View, Text, StyleSheet } from "react-native";
import { colors, borderRadius, typography, spacing } from "@/constants/theme";

type Props = {
  risk: number | null | undefined;
  size?: "small" | "medium" | "large";
  showLabel?: boolean;
};

export default function RiskBadge({ risk, size = "medium", showLabel = true }: Props) {
  const score = risk ?? 0;
  
  const getRiskLevel = () => {
    if (score >= 70) return { label: "Critical", color: colors.risk.critical, icon: "🔴" };
    if (score >= 50) return { label: "High", color: colors.risk.high, icon: "🟠" };
    if (score >= 30) return { label: "Medium", color: colors.risk.medium, icon: "🟡" };
    return { label: "Low", color: colors.risk.low, icon: "🟢" };
  };

  const { label, color, icon } = getRiskLevel();

  const sizeStyles = {
    small: { padding: spacing.xs, fontSize: 12 },
    medium: { padding: spacing.sm, fontSize: 14 },
    large: { padding: spacing.md, fontSize: 16 },
  };

  return (
    <View style={[styles.container, { backgroundColor: `${color}15` }]}>
      <View style={[styles.badge, { backgroundColor: color }, sizeStyles[size]]}>
        <Text style={[styles.badgeText, { fontSize: sizeStyles[size].fontSize }]}>
          {icon} {score}%
        </Text>
      </View>
      {showLabel && (
        <Text style={[styles.label, { color, fontSize: sizeStyles[size].fontSize }]}>
          {label} Risk
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    alignSelf: "flex-start",
    borderRadius: borderRadius.lg,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    gap: spacing.sm,
  },
  badge: {
    borderRadius: borderRadius.full,
    minWidth: 60,
    alignItems: "center",
  },
  badgeText: {
    color: colors.surface,
    fontWeight: "700",
  },
  label: {
    fontWeight: "600",
  },
});
