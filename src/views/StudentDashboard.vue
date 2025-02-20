<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import Sidebar from '@/components/Sidebar.vue';
import marksChart from '@/assets/marks_chart.png';
import doubtChart from '@/assets/instructor_doubts_chart.png';
</script>

<template>
    <NavbarMain />
    <div class="flex">
        <Sidebar />
        <div class="flex-1 flex flex-col items-center my-10 gap-6">
            <div class="w-[80%] h-fit px-12 py-18 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6 justify-center ">
                <span class="text-3xl mb-15">Assignments Due</span>
                <span class="text-center">No Pending Assignment</span>
            </div>

            <div class="w-[80%] h-fit px-12 py-18 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6 justify-center ">
                <div class="text-center">
                    <span class="text-3xl">Statistics</span>
                </div>

                <div class="flex justify-evenly">
                    <img :src="marksChart" alt="" class="w-[40%]">
                    <img :src="doubtChart" alt="" class="w-[40%]">

                </div>
            </div>
        </div>
    </div>

</template>