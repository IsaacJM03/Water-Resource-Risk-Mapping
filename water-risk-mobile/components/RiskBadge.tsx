
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const RiskBadge = ({ level }: { level: string }) => {
  return (
    <View style={styles.badge}>
      <Text>{level}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  badge: {
    padding: 8,
    borderRadius: 4,
    backgroundColor: 'red',
  },
});

export default RiskBadge;