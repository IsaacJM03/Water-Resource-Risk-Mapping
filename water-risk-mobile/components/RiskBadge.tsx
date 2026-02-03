import { View, Text, StyleSheet } from "react-native";

type Props = {
  risk: number;
};

export default function RiskBadge({ risk }: Props) {
  let bg = "#16a34a"; // green
  let label = "LOW";

  if (risk >= 40) {
    bg = "#eab308";
    label = "MEDIUM";
  }
  if (risk >= 70) {
    bg = "#f97316";
    label = "HIGH";
  }
  if (risk >= 85) {
    bg = "#dc2626";
    label = "CRITICAL";
  }

  return (
    <View style={[styles.badge, { backgroundColor: bg }]}>
      <Text style={styles.text}>
        {label} · {risk}%
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 999,
    alignSelf: "flex-start",
    marginBottom: 6,
  },
  text: {
    color: "#fff",
    fontSize: 12,
    fontWeight: "600",
  },
});
