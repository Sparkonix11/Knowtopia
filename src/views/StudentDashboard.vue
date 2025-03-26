<script setup>
import { ref, onMounted } from 'vue';
import BaseLayout from '@/components/BaseLayout.vue';
import StatCard from '@/components/StatCard.vue';
import { useStudentDashboard } from '@/handlers/useStudentDashboard';
import { Chart, registerables } from 'chart.js';
import { useRouter } from 'vue-router';

// Register Chart.js components
Chart.register(...registerables);

const router = useRouter();

// Use the student dashboard handler
const {
  assignmentMarks,
  chatDoubts,
  upcomingAssignments,
  isLoadingMarks,
  isLoadingDoubts,
  isLoadingAssignments,
  marksError,
  doubtsError,
  assignmentsError,
  fetchAssignmentMarks,
  fetchChatDoubts,
  fetchUpcomingAssignments,
  marksChartData,
  doubtsChartData
} = useStudentDashboard();

// References to chart canvases
const marksChartCanvas = ref(null);
const doubtsChartCanvas = ref(null);

// Chart instances
let marksChartInstance = null;
let doubtsChartInstance = null;

// Navigate to the assignment
const goToAssignment = (assignment) => {
  router.push({
    name: 'Course',
    params: { id: assignment.courseId },
    query: { assignmentId: assignment.id }
  });
};

// Format date for display
const formatDueDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });
};

// Fetch data and render charts on component mount
onMounted(async () => {
  try {
    // Fetch data for both charts and upcoming assignments
    await Promise.all([
      fetchAssignmentMarks(),
      fetchChatDoubts(),
      fetchUpcomingAssignments()
    ]);
    
    // Render the marks chart
    if (marksChartCanvas.value) {
      marksChartInstance = new Chart(marksChartCanvas.value, {
        type: 'bar',
        data: marksChartData.value,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              title: {
                display: true,
                text: 'Percentage Marks'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Topics'
              }
            }
          },
          plugins: {
            title: {
              display: true,
              text: 'Marks Scored in Different Topics'
            }
          }
        }
      });
    }
    
    // Render the doubts chart
    if (doubtsChartCanvas.value) {
      doubtsChartInstance = new Chart(doubtsChartCanvas.value, {
        type: 'line',
        data: doubtsChartData.value,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Number of Doubts'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Days'
              }
            }
          },
          plugins: {
            title: {
              display: true,
              text: 'Doubts Asked Over Time'
            }
          }
        }
      });
    }
  } catch (error) {
    console.error('Error initializing charts:', error);
  }
});
</script>

<template>
    <BaseLayout contentClass="my-10 gap-6">
        <StatCard title="Assignments Due" class="w-full">
            <div v-if="isLoadingAssignments" class="flex justify-center items-center h-16">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <div v-else-if="assignmentsError" class="p-4 bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) rounded-[12px] mb-4">
                <p>{{ assignmentsError }}</p>
            </div>
            
            <div v-else-if="upcomingAssignments.length === 0" class="text-center">
                <span>No Pending Assignment</span>
            </div>
            
            <div v-else class="grid grid-cols-1 gap-3">
                <div 
                    v-for="assignment in upcomingAssignments" 
                    :key="assignment.id"
                    class="p-3 border border-(--md-sys-color-outline-variant) rounded-[12px] cursor-pointer hover:bg-(--md-sys-color-surface-variant) transition-colors"
                    @click="goToAssignment(assignment)"
                >
                    <div class="flex items-center mb-1">
                        <md-icon class="mr-2 text-sm">assignment</md-icon>
                        <h3 class="font-semibold">{{ assignment.name }}</h3>
                    </div>
                    
                    <div class="flex flex-col text-sm text-(--md-sys-color-on-surface-variant)">
                        <div class="flex items-center mb-1">
                            <md-icon class="text-sm mr-1">book</md-icon>
                            <span>{{ assignment.courseName }}</span>
                        </div>
                        <div class="flex items-center">
                            <md-icon class="text-sm mr-1 text-(--md-sys-color-error)">schedule</md-icon>
                            <span class="text-(--md-sys-color-error)">Due: {{ formatDueDate(assignment.due_date) }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </StatCard>

        <StatCard title="Statistics" class="w-full">
            <div v-if="isLoadingMarks || isLoadingDoubts" class="flex justify-center items-center h-64">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <div v-else-if="marksError || doubtsError" class="p-4 bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) rounded-[12px] mb-4">
                <p>{{ marksError || doubtsError }}</p>
            </div>
            
            <div v-else class="flex flex-col md:flex-row justify-evenly gap-4">
                <div class="w-full md:w-[45%] h-[300px]">
                    <canvas ref="marksChartCanvas"></canvas>
                </div>
                <div class="w-full md:w-[45%] h-[300px]">
                    <canvas ref="doubtsChartCanvas"></canvas>
                </div>
            </div>
        </StatCard>
    </BaseLayout>
</template>