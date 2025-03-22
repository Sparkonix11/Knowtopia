<script setup>
import BaseLayout from '@/components/BaseLayout.vue';
import ReviewCard from '@/components/ReviewCard.vue';
import StatCard from '@/components/StatCard.vue';
import marksChart from '@/assets/instructor_marks_chart.png';
import doubtChart from '@/assets/instructor_doubts_chart.png';
</script>

<template>
<BaseLayout>
        <div class="w-[80%] h-fit px-12 py-18 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6">
            <div class="text-center">
                <span class="text-3xl">Reviews</span>
            </div>

            <div class="flex w-full justify-evenly">
                <ReviewCard 
                    username="User Name" 
                    :rating="4" 
                    review="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed rutrum ligula. Duis massa diam, mollis vel vehicula at, tempor et urna. Maecenas eget mi tortor. Maecenas a vehicula lorem."
                />
                
                <ReviewCard 
                    username="User Name 2" 
                    :rating="3" 
                    review="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed rutrum ligula. Duis massa diam, mollis vel vehicula at, tempor et urna. Maecenas eget mi tortor. Maecenas a vehicula lorem."
                />
                
                <ReviewCard 
                    username="User Name 3" 
                    :rating="5" 
                    review="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed rutrum ligula. Duis massa diam, mollis vel vehicula at, tempor et urna. Maecenas eget mi tortor. Maecenas a vehicula lorem."
                />
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