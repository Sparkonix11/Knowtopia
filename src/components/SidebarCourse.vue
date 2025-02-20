<script setup>
import { defineProps, ref } from 'vue';
const props = defineProps({
  lectures: {
    type: Array,
    required: true,
    default: () => []
  }
});

const openLectures = ref({});

const toggleLecture = (name) => {
  openLectures.value[name] = !openLectures.value[name];
};

</script>
<template>
    <div class="w-[20%] h-[calc(100vh-5rem)] px-3  rounded-[12px] bg-(--md-sys-color-surface-container-low)">
        <span class="px-4 py-8 block text-xl">Course Name</span>

        <div v-for="lecture in lectures" :key="lecture.name">
            <!-- Main lecture header -->
            <md-list class="rounded-[50px] border-1 border-(--md-sys-color-outline) ">
            <md-list-item @click="toggleLecture(lecture.name)" class=" cursor-pointer bg-(--md-sys-color-secondary-container) rounded-[100px] border-(--md-sys-color-outline) border-b-1 px-2">
                <div slot="start">
                    <md-icon>list</md-icon>
                </div>
                <span class="font-medium">{{ lecture.name }}</span>

                <div slot="end" class="flex gap-2 items-center">
                    <md-icon>{{ openLectures[lecture.name] ? 'expand_less' : 'expand_more' }}</md-icon>
                </div>
            </md-list-item>

            <!-- Sub lectures dropdown -->
            <div v-if="openLectures[lecture.name]" class="rounded-[50px]">
                <md-list-item 
                v-for="subLecture in lecture.subLectures" 
                :key="subLecture"
                class="rounded-[100px] px-6 border-b border-(--md-sys-color-outline-variant) hover:bg-(--md-sys-color-on-surface2)"
                >
                <router-link :to="subLecture === 'Assignment 1.1' ? { name: 'Assignment' } : { name: 'Course' }">
                    <label class="flex items-center gap-3">
                        <md-checkbox touch-target="wrapper"></md-checkbox>
                        {{ subLecture }}
                    </label>
                </router-link>
                </md-list-item>

            </div>
            
            </md-list>
        </div>
    </div>
</template>