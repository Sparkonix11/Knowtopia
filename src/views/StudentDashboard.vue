<script setup>
import BaseLayout from '@/components/BaseLayout.vue';
import StatCard from '@/components/StatCard.vue';
import marksChart from '@/assets/marks_chart.png';
import doubtChart from '@/assets/instructor_doubts_chart.png';
</script>

<template>
    <BaseLayout>
            <StatCard title="Assignments Due">
                <span class="text-center">No Pending Assignment</span>
            </StatCard>

            <StatCard title="Statistics">
                <div class="flex justify-evenly">
                    <img :src="marksChart" alt="" class="w-[40%]">
                    <img :src="doubtChart" alt="" class="w-[40%]">
                </div>
            </StatCard>
    </BaseLayout>

</template>