<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import SidebarCourse from '@/components/SidebarCourse.vue';
import placeholder from '@/assets/resource_placeholder.png';
import marksChart from '@/assets/marks_chart.png';
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const assignmentId = ref(null);
const score = ref(null);
const isLoading = ref(true);
const error = ref(null);

// Get score data either from route params or from API
onMounted(async () => {
  try {
    assignmentId.value = route.query.id || route.params.id;
    
    // If score data is passed in route query params, use it
    if (route.query.score && route.query.total) {
      score.value = {
        correct: parseInt(route.query.score),
        total: parseInt(route.query.total),
        percentage: parseFloat(route.query.percentage),
        submitted_at: new Date().toISOString()
      };
      isLoading.value = false;
      return;
    }
    
    // Otherwise fetch from API
    if (!assignmentId.value) {
      error.value = 'Assignment ID is missing';
      isLoading.value = false;
      return;
    }
    
    // Fetch score from API
    const response = await axios.get(`/api/v1/assignment/score/${assignmentId.value}`);
    
    if (response.data && response.data.score) {
      score.value = response.data.score;
    }
    
    isLoading.value = false;
  } catch (err) {
    console.error('Error fetching score:', err);
    error.value = err.message || 'Failed to load assignment score';
    isLoading.value = false;
  }
});

// Format the score percentage for display
const formattedPercentage = computed(() => {
  if (!score.value) return '0%';
  return `${Math.round(score.value.percentage)}%`;
});

// Format the submission date
const formattedDate = computed(() => {
  if (!score.value || !score.value.submitted_at) return '';
  return new Date(score.value.submitted_at).toLocaleString();
});
</script>
<template>
    <NavbarMain />
    <div class="flex">
        <SidebarCourse :lectures="lecturedata.lectures"/>

        <div class="flex-1 flex flex-col items-center my-10 gap-6">
            <div v-if="isLoading" class="flex justify-center items-center h-64">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <div v-else-if="error" class="w-[80%] p-6 bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) rounded-[12px]">
                <p>{{ error }}</p>
            </div>
            
            <div v-else-if="!score" class="w-[80%] p-6 bg-(--md-sys-color-secondary-container) text-(--md-sys-color-on-secondary-container) rounded-[12px]">
                <p>You have not submitted this assignment yet.</p>
            </div>
            
            <div v-else class="w-[80%] h-fit p-12 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6">
                <div class="text-center"><span class="text-3xl">Assignment Report</span></div>
                
                <div class="flex flex-col gap-4 mt-8">
                    <div class="flex justify-between items-center p-4 bg-(--md-sys-color-surface-variant) rounded-[12px]">
                        <span class="text-xl font-medium">Score:</span>
                        <span class="text-xl">{{ score.correct }} / {{ score.total }}</span>
                    </div>
                    
                    <div class="flex justify-between items-center p-4 bg-(--md-sys-color-surface-variant) rounded-[12px]">
                        <span class="text-xl font-medium">Percentage:</span>
                        <span class="text-xl">{{ formattedPercentage }}</span>
                    </div>
                    
                    <div class="flex justify-between items-center p-4 bg-(--md-sys-color-surface-variant) rounded-[12px]">
                        <span class="text-xl font-medium">Submitted on:</span>
                        <span class="text-xl">{{ formattedDate }}</span>
                    </div>
                </div>
                
                <div class="mt-6 p-4 bg-(--md-sys-color-primary-container) text-(--md-sys-color-on-primary-container) rounded-[12px] text-center">
                    <p class="text-xl" v-if="score.percentage >= 70">Excellent work! You've mastered this assignment.</p>
                    <p class="text-xl" v-else-if="score.percentage >= 50">Good job! You're on the right track.</p>
                    <p class="text-xl" v-else>Keep practicing! You'll improve with more study.</p>
                </div>
                
                <div class="flex justify-center mt-6">
                    <router-link :to="{name: 'Course'}">
                        <md-filled-button>Back to Course</md-filled-button>
                    </router-link>
                </div>
            </div> 
        </div>
    </div>
</template>

<script>
const lecturedata = {
    "lectures": [
    {
      "name": "Lecture 1",
      "subLectures": ["Lecture 1.1", "Lecture 1.2", "Assignment 1.1"]
    },
    {
      "name": "Lecture 2",
      "subLectures": ["Lecture 2.1", "Lecture 2.2"]
    },
    {
      "name": "Lecture 3",
      "subLectures": ["Lecture 3.1"]
    }
  ]
};
</script>