<script setup>
import NavBarMain from '@/components/NavBarMain.vue';
import SidebarCourse from '@/components/SidebarCourse.vue';
import placeholder from '@/assets/placeholder.mp4';
import WriteReview from '@/components/WriteReview.vue';
import Summaries from '@/components/Summaries.vue';

import { ref } from "vue";
const showWriteReview = ref(false);
const showSummaries = ref(false);

const toggleWriteReview = () => {
    showWriteReview.value = !showWriteReview.value;
};
const toggleSummaries = () => {
    showSummaries.value = !showSummaries.value;
};
</script>

<template>
    <NavBarMain />
    <div class="flex">
        <SidebarCourse :lectures="lecturedata.lectures"/>
        <div class="flex-1 flex flex-col items-center my-10 gap-6">
            <video class="w-[80%] rounded-[12px] border border-(--md-sys-color-outline)" controls>
                <source :src="placeholder" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div class="flex justify-between w-[78%]">
                <span class=" text-3xl">Topic Name</span>
                <div class="flex gap-2">
                    <md-outlined-button class="w-33 h-10" @click="toggleWriteReview">Write Review</md-outlined-button>
                    <md-outlined-button class="w-33 h-10" @click="toggleSummaries">Summarise</md-outlined-button>
                </div>
            </div>
            <span class="w-[78%]">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris vestibulum accumsan mauris, a vulputate magna volutpat eu. Integer ornare sollicitudin nunc. In nec sollicitudin mauris, in pharetra nunc. Proin orci odio, varius nec nibh id, facilisis porttitor justo. In porta ornare dapibus. Proin ac tortor sit amet nunc vestibulum viverr</span>
        </div>
    </div>

    <WriteReview v-if="showWriteReview" @toggleWriteReview="toggleWriteReview"/>
    <Summaries v-if="showSummaries" @toggleSummaries="toggleSummaries" />
    
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