<script setup>
import { ref, onMounted } from 'vue';
import BaseLayout from '@/components/BaseLayout.vue';
import ReviewCard from '@/components/ReviewCard.vue';
import StatCard from '@/components/StatCard.vue';
import marksChart from '@/assets/instructor_marks_chart.png';
import doubtChart from '@/assets/instructor_doubts_chart.png';
import { fetchInstructorReviewsAPI } from '@/services/operations/reviewAPI';

const reviews = ref([]);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
    try {
        loading.value = true;
        const response = await fetchInstructorReviewsAPI();
        if (response.data && response.data.reviews) {
            reviews.value = response.data.reviews;
        }
    } catch (err) {
        console.error('Error fetching reviews:', err);
        error.value = 'Failed to load reviews. Please try again later.';
    } finally {
        loading.value = false;
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

        <StatCard title="Statistics">
            <div class="flex justify-evenly">
                <img :src="marksChart" alt="" class="w-[40%]">
                <img :src="doubtChart" alt="" class="w-[40%]">
            </div>
        </StatCard>
</BaseLayout>
</template>