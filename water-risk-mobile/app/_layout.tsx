import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';
import { AuthProvider } from "@/context/AuthContext";
import * as Notifications from "expo-notifications";
import { useEffect } from "react";
import { Platform } from "react-native";
import { useColorScheme } from '@/hooks/use-color-scheme';

export const unstable_settings = {
  anchor: '(tabs)',
};

export default function RootLayout() {
  const colorScheme = useColorScheme();
  useEffect(() => {
    async function register() {
      const { status } = await Notifications.requestPermissionsAsync();
      if (status !== "granted") return;
  
      const token = (await Notifications.getExpoPushTokenAsync()).data;
      console.log("Push token:", token);
  
      // TODO: send token to backend
    }
  
    register();
  }, []);
  
  return (
    <AuthProvider>
      <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
        <Stack screenOptions={{ headerShown: false }}>
          <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
          <Stack.Screen 
            name="sources/[id]" 
            options={{ 
              title: "Source Details",
              headerShown: true,
              headerBackTitle: "Back",
            }} 
          />
          <Stack.Screen name="modal" options={{ presentation: 'modal', title: 'Modal' }} />
        </Stack>
        <StatusBar style="auto" />
      </ThemeProvider>
    </AuthProvider>
  );
}
