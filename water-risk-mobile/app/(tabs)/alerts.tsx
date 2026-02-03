import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, useColorScheme, ActivityIndicator, TouchableOpacity, RefreshControl } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { alertsApi, Alert } from '../../services/apiClient';

export default function AlertsScreen() {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';

  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      setError(null);
      const data = await alertsApi.getAll();
      setAlerts(data);
    } catch (err) {
      console.error('Failed to load alerts:', err);
      setError('Failed to load alerts. Please check your connection.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadAlerts();
  };

  const handleAcknowledge = async (alertId: number) => {
    try {
      await alertsApi.acknowledge(alertId);
      setAlerts((prev) =>
        prev.map((alert) =>
          alert.id === alertId ? { ...alert, acknowledged: true } : alert
        )
      );
    } catch (err) {
      console.error('Failed to acknowledge alert:', err);
    }
  };

  const getLevelStyle = (level: string) => {
    const levelLower = level.toLowerCase();
    const styles = {
      critical: { color: '#dc2626', icon: '🔴' },
      high: { color: '#ef4444', icon: '🟠' },
      medium: { color: '#f59e0b', icon: '🟡' },
      low: { color: '#10b981', icon: '🟢' },
    };
    return styles[levelLower as keyof typeof styles] || styles.low;
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  };

  if (loading) {
    return (
      <View style={[styles.container, styles.centered, { backgroundColor: isDark ? '#111827' : '#f3f4f6' }]}>
        <ActivityIndicator size="large" color="#3b82f6" />
        <Text style={[styles.loadingText, { color: isDark ? '#9ca3af' : '#6b7280' }]}>
          Loading alerts...
        </Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={[styles.container, styles.centered, { backgroundColor: isDark ? '#111827' : '#f3f4f6' }]}>
        <Ionicons name="alert-circle" size={48} color="#ef4444" />
        <Text style={[styles.errorText, { color: isDark ? '#f9fafb' : '#111827' }]}>
          {error}
        </Text>
        <TouchableOpacity style={styles.retryButton} onPress={loadAlerts}>
          <Text style={styles.retryButtonText}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const unacknowledgedCount = alerts.filter(a => !a.acknowledged).length;

  return (
    <View style={[styles.container, { backgroundColor: isDark ? '#111827' : '#f3f4f6' }]}>
      <View style={[styles.header, { backgroundColor: isDark ? '#1f2937' : '#ffffff' }]}>
        <Text style={[styles.headerTitle, { color: isDark ? '#f9fafb' : '#111827' }]}>
          Active Alerts
        </Text>
        {unacknowledgedCount > 0 && (
          <View style={styles.badge}>
            <Text style={styles.badgeText}>{unacknowledgedCount}</Text>
          </View>
        )}
      </View>

      <FlatList
        data={alerts}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => {
          const levelStyle = getLevelStyle(item.level);
          return (
            <View style={[
              styles.alertCard,
              { 
                backgroundColor: isDark ? '#1f2937' : '#ffffff',
                borderLeftColor: levelStyle.color,
                opacity: item.acknowledged ? 0.6 : 1,
              }
            ]}>
              <View style={styles.alertHeader}>
                <View style={styles.alertLevel}>
                  <Text style={styles.levelIcon}>{levelStyle.icon}</Text>
                  <Text style={[styles.levelText, { color: levelStyle.color }]}>
                    {item.level.toUpperCase()}
                  </Text>
                </View>
                <Text style={[styles.alertTime, { color: isDark ? '#9ca3af' : '#6b7280' }]}>
                  {formatTime(item.created_at)}
                </Text>
              </View>

              <Text style={[styles.alertMessage, { color: isDark ? '#d1d5db' : '#4b5563' }]}>
                {item.message}
              </Text>

              {!item.acknowledged && (
                <TouchableOpacity
                  style={styles.acknowledgeButton}
                  onPress={() => handleAcknowledge(item.id)}
                >
                  <Text style={styles.acknowledgeButtonText}>✓ Acknowledge</Text>
                </TouchableOpacity>
              )}
            </View>
          );
        }}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor={isDark ? '#9ca3af' : '#6b7280'}
          />
        }
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Ionicons name="checkmark-circle" size={64} color={isDark ? '#4b5563' : '#d1d5db'} />
            <Text style={[styles.emptyText, { color: isDark ? '#9ca3af' : '#6b7280' }]}>
              No alerts at this time
            </Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  centered: { justifyContent: 'center', alignItems: 'center' },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 60,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  headerTitle: { fontSize: 28, fontWeight: 'bold' },
  badge: {
    backgroundColor: '#ef4444',
    borderRadius: 9999,
    minWidth: 28,
    height: 28,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 8,
  },
  badgeText: { color: '#ffffff', fontSize: 14, fontWeight: '700' },
  listContent: { padding: 16 },
  alertCard: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  alertHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  alertLevel: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  levelIcon: { fontSize: 16 },
  levelText: { fontSize: 14, fontWeight: '700' },
  alertTime: { fontSize: 12 },
  alertMessage: { fontSize: 14, lineHeight: 20, marginBottom: 12 },
  acknowledgeButton: {
    backgroundColor: '#3b82f6',
    padding: 10,
    borderRadius: 8,
    alignItems: 'center',
  },
  acknowledgeButtonText: { color: '#ffffff', fontSize: 14, fontWeight: '600' },
  loadingText: { marginTop: 16, fontSize: 16 },
  errorText: { marginTop: 16, fontSize: 16, textAlign: 'center', paddingHorizontal: 32 },
  retryButton: {
    marginTop: 16,
    backgroundColor: '#3b82f6',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  retryButtonText: { color: '#ffffff', fontSize: 16, fontWeight: '600' },
  emptyState: { alignItems: 'center', marginTop: 64 },
  emptyText: { marginTop: 16, fontSize: 16 },
});
