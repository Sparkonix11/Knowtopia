<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import SidebarCourse from '@/components/SidebarCourse.vue';
import placeholder from '@/assets/resource_placeholder.png';
import marksChart from '@/assets/marks_chart.png';
</script>
<template>
    <NavbarMain />
    <div class="flex">
        <SidebarCourse :lectures="lecturedata.lectures"/>

        <div class="flex-1 flex flex-col items-center my-10 gap-6">
            <div class="w-[80%] h-fit p-12 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6">
                <div class="text-center"><span class="text-3xl">Report</span></div>
                <div class="flex gap-4 justify-around mt-8">
                    <img :src="placeholder" alt="" class="w-75 h-75 rounded-[12px] border border-(--md-sys-color-outline)">
                    <img :src="placeholder" alt="" class="w-75 h-75 rounded-[12px] border border-(--md-sys-color-outline)">
                    <img :src="placeholder" alt="" class="w-75 h-75 rounded-[12px] border border-(--md-sys-color-outline)">
                    <img :src="placeholder" alt="" class="w-75 h-75 rounded-[12px] border border-(--md-sys-color-outline)">

                </div>
                <div class=" justify-between items-center w-full">
                    <img :src="marksChart" alt="" class="w-225 h-125 m-auto rounded-[12px] border border-(--md-sys-color-outline-variant)">
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