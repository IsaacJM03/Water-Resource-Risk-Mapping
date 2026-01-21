import { apiClient } from "@/services/apiClient";
import { fetchSources } from "@/services/sources";
import React, { useEffect } from "react";
import { View, Text } from "react-native";


export default function Index() {
  useEffect(() => {
    apiClient.get("/health")
      .then((data) => {
        console.log("Health check:", data);
      })
      .catch(console.error);
  }, []);
  useEffect(() => {
    fetchSources()
      .then((sources) => {
        console.log("Sources:", sources);
      })
      .catch(console.error);
  }, []);
  

  return (
    <View>
      <Text>Dashboard</Text>
    </View>
  );
}
// import React from 'react';
// import { View, Text, StyleSheet } from 'react-native';

// const Dashboard = () => {
//   return (
//     <View style={styles.container}>
//       <Text>Dashboard</Text>
//     </View>
//   );
// };

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     justifyContent: 'center',
//     alignItems: 'center',
//   },
// });

// export default Dashboard;
