import { ref } from 'vue';
import { searchAPI } from '@/services/operations/searchAPI';
import { useRouter } from 'vue-router';

export const useSearch = () => {
  const searchResults = ref([]);
  const isLoading = ref(false);
  const error = ref(null);
  const totalResults = ref(0);
  const router = useRouter();

  const performSearch = async (query) => {
    if (!query || query.trim().length < 3) {
      error.value = 'Search query must be at least 3 characters long';
      return;
    }

    try {
      isLoading.value = true;
      error.value = null;
      
      const data = await searchAPI(query);
      
      searchResults.value = data.results;
      totalResults.value = data.count;
      
      // Navigate to search results page with the query
      router.push({ name: 'SearchResults', query: { q: query } });
    } catch (err) {
      console.error('Search error:', err);
      error.value = err.response?.data?.message || 'An error occurred during search';
      searchResults.value = [];
      totalResults.value = 0;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    searchResults,
    isLoading,
    error,
    totalResults,
    performSearch
  };
};