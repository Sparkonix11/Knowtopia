<script setup>
import { ref, onMounted } from 'vue';
import BaseLayout from '@/components/BaseLayout.vue';
import StatCard from '@/components/StatCard.vue';
import { useStudentDashboard } from '@/handlers/useStudentDashboard';
import { Chart, registerables } from 'chart.js';

// Register Chart.js components
Chart.register(...registerables);

// Use the student dashboard handler
const {
  assignmentMarks,
  chatDoubts,
  isLoadingMarks,
  isLoadingDoubts,
  marksError,
  doubtsError,
  fetchAssignmentMarks,
  fetchChatDoubts,
  marksChartData,
  doubtsChartData
} = useStudentDashboard();

// References to chart canvases
const marksChartCanvas = ref(null);
const doubtsChartCanvas = ref(null);

// Chart instances
let marksChartInstance = null;
let doubtsChartInstance = null;

// Fetch data and render charts on component mount
onMounted(async () => {
  try {
    // Fetch data for both charts
    await Promise.all([
      fetchAssignmentMarks(),
      fetchChatDoubts()
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
            <span class="text-center">No Pending Assignment</span>
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