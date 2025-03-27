<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import NavBarMain from '@/components/NavBarMain.vue';
import Sidebar from '@/components/Sidebar.vue';
import { useSearch } from '@/handlers/useSearch';

const route = useRoute();
const router = useRouter();
const query = computed(() => route.query.q || '');

const { searchResults, isLoading, error, totalResults, performSearch } = useSearch();

// Perform search when component mounts or query changes
onMounted(async () => {
  if (query.value) {
    await performSearch(query.value);
  }
});

// Navigate to appropriate page based on result type
const navigateToResult = (result) => {
  if (result.type === 'course') {
    router.push({ name: 'Course', params: { id: result.id } });
  } else if (result.type === 'material') {
    // Navigate to course view with the material highlighted
    router.push({ 
      name: 'Course', 
      params: { id: result.course_id },
      query: { materialId: result.id }
    });
  } else if (result.type === 'assignment') {
    router.push({ name: 'Assignment', params: { id: result.id } });
  }
};
</script>

<template>
  <div>
    <NavBarMain />
    <div class="flex">
      <Sidebar />
      <div class="ml-90 p-8 w-[calc(100%-90px)]">
        <div class="mb-6">
          <h1 class="text-2xl font-bold mb-2">Search Results for "{{ query }}"</h1>
          <p v-if="totalResults > 0" class="text-gray-600">{{ totalResults }} results found</p>
          <p v-else-if="!isLoading && !error" class="text-gray-600">No results found</p>
          <p v-if="error" class="text-red-500">{{ error }}</p>
        </div>

        <!-- Loading state -->
        <div v-if="isLoading" class="flex justify-center items-center h-40">
          <md-circular-progress indeterminate></md-circular-progress>
        </div>

        <!-- Results list -->
        <div v-else class="space-y-4">
          <div v-for="result in searchResults" :key="`${result.type}-${result.id}`" 
               @click="navigateToResult(result)"
               class="p-4 border rounded-lg cursor-pointer hover:bg-(--md-sys-color-surface-container-high) transition-colors">
            
            <!-- Course result -->
            <div v-if="result.type === 'course'" class="flex items-start">
              <div class="mr-4 p-2 rounded-full bg-(--md-sys-color-primary-container)">
                <md-icon>school</md-icon>
              </div>
              <div>
                <h3 class="text-lg font-semibold">{{ result.name }}</h3>
                <p class="text-sm text-gray-600">Course</p>
                <p class="mt-1">{{ result.description }}</p>
              </div>
            </div>

            <!-- Material result -->
            <div v-else-if="result.type === 'material'" class="flex items-start">
              <div class="mr-4 p-2 rounded-full bg-(--md-sys-color-secondary-container)">
                <md-icon>menu_book</md-icon>
              </div>
              <div>
                <h3 class="text-lg font-semibold">{{ result.title }}</h3>
                <p class="text-sm text-gray-600">Study Material</p>
                <p class="mt-1">{{ result.description }}</p>
              </div>
            </div>

            <!-- Assignment result -->
            <div v-else-if="result.type === 'assignment'" class="flex items-start">
              <div class="mr-4 p-2 rounded-full bg-(--md-sys-color-tertiary-container)">
                <md-icon>assignment</md-icon>
              </div>
              <div>
                <h3 class="text-lg font-semibold">{{ result.title }}</h3>
                <p class="text-sm text-gray-600">Assignment</p>
                <p class="mt-1">{{ result.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>