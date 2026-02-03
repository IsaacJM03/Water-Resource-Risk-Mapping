import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, useColorScheme, TextInput, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface WaterSource {
  id: string;
  name: string;
  location: string;
  riskLevel: 'high' | 'medium' | 'low';
  waterLevel: number;
  rainfall: number;
}

const MOCK_SOURCES: WaterSource[] = [
  { id: '1', name: 'Lake Victoria', location: 'Central Region', riskLevel: 'high', waterLevel: 15.2, rainfall: 45.3 },
  { id: '2', name: 'River Nile', location: 'Northern Region', riskLevel: 'medium', waterLevel: 22.8, rainfall: 62.1 },
  { id: '3', name: 'Lake Albert', location: 'Western Region', riskLevel: 'low', waterLevel: 18.5, rainfall: 78.4 },
  { id: '4', name: 'Lake Kyoga', location: 'Eastern Region', riskLevel: 'medium', waterLevel: 20.1, rainfall: 55.7 },
];

export default function ExploreScreen() {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';
  const [searchQuery, setSearchQuery] = useState('');

  const filteredSources = MOCK_SOURCES.filter(source =>
    source.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    source.location.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: isDark ? '#111827' : '#f3f4f6' }]}>
      <View style={[styles.header, { backgroundColor: isDark ? '#1f2937' : '#ffffff' }]}>
        <Text style={[styles.headerTitle, { color: isDark ? '#f9fafb' : '#111827' }]}>
          Explore Water Sources
        </Text>
        
        <View style={[
          styles.searchContainer,
          { backgroundColor: isDark ? '#374151' : '#f3f4f6' }
        ]}>
          <Ionicons name="search" size={20} color={isDark ? '#9ca3af' : '#6b7280'} />
          <TextInput
            style={[styles.searchInput, { color: isDark ? '#f9fafb' : '#111827' }]}
            placeholder="Search sources or locations..."
            placeholderTextColor={isDark ? '#6b7280' : '#9ca3af'}
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.statsRow}>
          <View style={[styles.statCard, { backgroundColor: isDark ? '#1f2937' : '#ffffff' }]}>
            <Ionicons name="water" size={24} color="#3b82f6" />
            <Text style={[styles.statNumber, { color: isDark ? '#f9fafb' : '#111827' }]}>
              {MOCK_SOURCES.length}
            </Text>
            <Text style={[styles.statLabel, { color: isDark ? '#9ca3af' : '#6b7280' }]}>
              Total Sources
            </Text>
          </View>

          <View style={[styles.statCard, { backgroundColor: isDark ? '#1f2937' : '#ffffff' }]}>
            <Ionicons name="alert-circle" size={24} color="#ef4444" />
            <Text style={[styles.statNumber, { color: isDark ? '#f9fafb' : '#111827' }]}>
              {MOCK_SOURCES.filter(s => s.riskLevel === 'high').length}
            </Text>
            <Text style={[styles.statLabel, { color: isDark ? '#9ca3af' : '#6b7280' }]}>
              High Risk
            </Text>
          </View>
        </View>

        <Text style={[styles.sectionTitle, { color: isDark ? '#f9fafb' : '#111827' }]}>
          Water Sources
        </Text>

        {filteredSources.map((source) => (
          <TouchableOpacity
            key={source.id}
            style={[styles.sourceCard, { backgroundColor: isDark ? '#1f2937' : '#ffffff' }]}
          >
            <View style={styles.sourceHeader}>
              <View style={{ flex: 1 }}>
                <Text style={[styles.sourceName, { color: isDark ? '#f9fafb' : '#111827' }]}>
                  {source.name}
                </Text>
                <Text style={[styles.sourceLocation, { color: isDark ? '#9ca3af' : '#6b7280' }]}>
                  <Ionicons name="location" size={12} /> {source.location}
                </Text>
              </View>
              <View style={[styles.riskBadge, { backgroundColor: getRiskColor(source.riskLevel) + '20' }]}>
                <Text style={[styles.riskText, { color: getRiskColor(source.riskLevel) }]}>
                  {source.riskLevel.toUpperCase()}
                </Text>
              </View>
            </View>

            <View style={styles.sourceMetrics}>
              <View style={styles.metric}>
                <Ionicons name="water-outline" size={16} color={isDark ? '#9ca3af' : '#6b7280'} />
                <Text style={[styles.metricLabel, { color: isDark ? '#9ca3af' : '#6b7280' }]}>
                  Water Level
                </Text>
                <Text style={[styles.metricValue, { color: isDark ? '#f9fafb' : '#111827' }]}>
                  {source.waterLevel}m
                </Text>
              </View>

              <View style={styles.metric}>
                <Ionicons name="rainy-outline" size={16} color={isDark ? '#9ca3af' : '#6b7280'} />
                <Text style={[styles.metricLabel, { color: isDark ? '#9ca3af' : '#6b7280' }]}>
                  Rainfall
                </Text>
                <Text style={[styles.metricValue, { color: isDark ? '#f9fafb' : '#111827' }]}>
                  {source.rainfall}mm
                </Text>
              </View>
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    padding: 20,
    paddingTop: 60,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 12,
    padding: 12,
    gap: 8,
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
  },
  content: {
    padding: 16,
  },
  statsRow: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  statCard: {
    flex: 1,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    marginTop: 4,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 16,
  },
  sourceCard: {
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sourceHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  sourceName: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 4,
  },
  sourceLocation: {
    fontSize: 14,
  },
  riskBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  riskText: {
    fontSize: 12,
    fontWeight: '600',
  },
  sourceMetrics: {
    flexDirection: 'row',
    gap: 24,
  },
  metric: {
    flex: 1,
    gap: 4,
  },
  metricLabel: {
    fontSize: 12,
  },
  metricValue: {
    fontSize: 16,
    fontWeight: '600',
  },
});
