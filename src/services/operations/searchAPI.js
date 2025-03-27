import { apiConnector } from '../apiConnector';
import { searchEndpoints } from '../apis';

const { SEARCH } = searchEndpoints;

export const searchAPI = async (query) => {
  try {
    const response = await apiConnector('GET', SEARCH, null, null, { query });
    return response.data;
  } catch (error) {
    console.error('Error in search API:', error);
    throw error;
  }
};