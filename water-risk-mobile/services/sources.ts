import apiClient from './apiClient';

export const getSources = async () => {
  const response = await apiClient.get('/sources');
  return response.data;
};
