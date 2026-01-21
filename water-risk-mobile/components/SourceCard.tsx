
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const SourceCard = ({ name }: { name: string }) => {
  return (
    <View style={styles.card}>
      <Text>{name}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    marginBottom: 8,
  },
});

export default SourceCard;