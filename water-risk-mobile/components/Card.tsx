import { View, StyleSheet, ViewStyle } from "react-native";
import { colors, borderRadius, spacing, shadows } from "@/constants/theme";

type Props = {
  children: React.ReactNode;
  style?: ViewStyle;
  variant?: "default" | "elevated" | "outlined";
};

export default function Card({ children, style, variant = "elevated" }: Props) {
  const variantStyles = {
    default: {},
    elevated: shadows.md,
    outlined: { borderWidth: 1, borderColor: colors.border },
  };

  return (
    <View style={[styles.card, variantStyles[variant], style]}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
  },
});