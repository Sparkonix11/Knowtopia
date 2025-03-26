<script setup>
import { ref, onMounted, nextTick } from 'vue';
import BaseLayout from '@/components/BaseLayout.vue';
import ReviewCard from '@/components/ReviewCard.vue';
import StatCard from '@/components/StatCard.vue';
import { fetchInstructorReviewsAPI } from '@/services/operations/reviewAPI';
import { useInstructorDashboard } from '@/handlers/useInstructorDashboard';
import { Chart, registerables } from 'chart.js';

// Register Chart.js components
Chart.register(...registerables);
console.log('Chart.js registered');

// Use the instructor dashboard handler
const {
  averageMarks,
  studentDoubts,
  isLoadingMarks,
  isLoadingDoubts,
  marksError,
  doubtsError,
  fetchAverageMarks,
  fetchStudentDoubts,
  marksChartData,
  doubtsChartData
} = useInstructorDashboard();
console.log('useInstructorDashboard initialized');

// References to chart canvases
const marksChartCanvas = ref(null);
const doubtsChartCanvas = ref(null);

// Chart instances
let marksChartInstance = null;
let doubtsChartInstance = null;

const reviews = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
    try {
        // Fetch reviews
        loading.value = true;
        const response = await fetchInstructorReviewsAPI();
        if (response.data && response.data.reviews) {
            reviews.value = response.data.reviews;
            console.log('Reviews fetched successfully:', reviews.value.length);
        }
    } catch (err) {
        console.error('Error fetching reviews:', err);
        error.value = 'Failed to load reviews. Please try again later.';
    } finally {
        loading.value = false;
    }
    
    // Fetch real data from API
    try {
        console.log('Fetching real data for charts');
        
        // Fetch assignment marks data
        await fetchAverageMarks();
        console.log('Average marks data fetched successfully:', averageMarks.value);
        
        // Fetch student doubts data
        await fetchStudentDoubts();
        console.log('Student doubts data fetched successfully:', studentDoubts.value);
        
        // Wait for the DOM to update
        await nextTick();
        
        console.log('DOM updated, checking for chart canvases');
        console.log('marksChartCanvas exists:', !!marksChartCanvas.value);
        console.log('doubtsChartCanvas exists:', !!doubtsChartCanvas.value);
        
        // Render the marks chart
        if (marksChartCanvas.value) {
            console.log('Rendering marks chart with real data');
            
            try {
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
                                    text: 'Average Marks (%)'
                                }
                            },
                            x: {
                                ticks: {
                                    maxRotation: 45,
                                    minRotation: 45
                                },
                                title: {
                                    display: true,
                                    text: 'Assignments (Course - Week)'
                                }
                            }
                        },
                        plugins: {
                            title: {
                                display: true,
                                text: 'Average Marks by Assignment'
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const assignment = mockAverageMarks[context.dataIndex];
                                        return [
                                            `Average: ${assignment.averageScore.toFixed(1)}%`,
                                            `Submissions: ${assignment.submissionCount}`
                                        ];
                                    }
                                }
                            }
                        }
                    }
                });
                console.log('Marks chart created successfully');
            } catch (chartError) {
                console.error('Error creating marks chart:', chartError);
            }
        } else {
            console.error('marksChartCanvas not found in the DOM');
            // Try to find the canvas by ID
            const canvasElement = document.getElementById('marksChart');
            console.log('Found marksChart by ID:', !!canvasElement);
        }
        
        // Render the doubts chart
        if (doubtsChartCanvas.value) {
            console.log('Rendering doubts chart with real data');
            
            try {
                doubtsChartInstance = new Chart(doubtsChartCanvas.value, {
                    type: 'bar',
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
                                ticks: {
                                    maxRotation: 45,
                                    minRotation: 45
                                },
                                title: {
                                    display: true,
                                    text: 'Materials (Course)'
                                }
                            }
                        },
                        plugins: {
                            title: {
                                display: true,
                                text: 'Student Doubts by Material'
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const material = mockStudentDoubts[context.dataIndex];
                                        return [
                                            `Doubts: ${material.doubtsCount}`,
                                            `Week: ${material.weekName}`
                                        ];
                                    }
                                }
                            }
                        }
                    }
                });
                console.log('Doubts chart created successfully');
            } catch (chartError) {
                console.error('Error creating doubts chart:', chartError);
            }
        } else {
            console.error('doubtsChartCanvas not found in the DOM');
            // Try to find the canvas by ID
            const canvasElement = document.getElementById('doubtsChart');
            console.log('Found doubtsChart by ID:', !!canvasElement);
        }
    } catch (error) {
        console.error('Error initializing charts:', error);
    }
});
</script>

<template>
<BaseLayout>
        <div class="w-[80%] h-fit px-12 py-18 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6">
            <div class="text-center">
                <span class="text-3xl">Reviews</span>
            </div>

            <div v-if="loading" class="text-center py-8">
                <p>Loading reviews...</p>
            </div>
            
            <div v-else-if="error" class="text-center py-8 text-red-500">
                <p>{{ error }}</p>
            </div>
            
            <div v-else-if="reviews.length === 0" class="text-center py-8">
                <p>No reviews found for your courses.</p>
            </div>
            
            <div v-else class="flex w-full flex-wrap justify-evenly gap-4">
                <div v-for="review in reviews" :key="review.id" class="w-full md:w-[30%]">
                    <ReviewCard 
                        :username="review.username" 
                        :rating="review.rating" 
                        :review="review.comment"
                        :userImage="review.user_image"
                    />
                    <div class="mt-2 text-sm text-gray-600">
                        <p>Course: {{ review.course_name }}</p>
                        <p>Material: {{ review.material_name }}</p>
                    </div>
                </div>
            </div>
        </div>

        <StatCard title="Statistics" class="w-full">
            <div v-if="isLoadingMarks || isLoadingDoubts" class="flex justify-center items-center h-64">
                <p>Loading chart data...</p>
            </div>
            
            <div v-else-if="marksError || doubtsError" class="p-4 bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) rounded-[12px] mb-4">
                <p>{{ marksError || doubtsError }}</p>
                <p class="mt-2">Check console for detailed error information</p>
            </div>
            
            <div v-else class="flex flex-col md:flex-row justify-evenly gap-4">
                <div class="w-full md:w-[45%] h-[300px]">
                    <canvas ref="marksChartCanvas" id="marksChart"></canvas>
                    <div v-if="averageMarks.length === 0" class="text-center py-4">
                        No marks data available
                    </div>
                </div>
                <div class="w-full md:w-[45%] h-[300px]">
                    <canvas ref="doubtsChartCanvas" id="doubtsChart"></canvas>
                    <div v-if="studentDoubts.length === 0" class="text-center py-4">
                        No doubts data available
                    </div>
                </div>
            </div>
        </StatCard>
</BaseLayout>
</template>