import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const SourceDetail = () => {
  return (
    <View style={styles.container}>
      <Text>Water Source Detail</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default SourceDetail;
