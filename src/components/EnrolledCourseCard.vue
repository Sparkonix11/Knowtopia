<script setup>
const props = defineProps({
    courseId: String,
    courseName: String,
    description: String,
    thumbnail: String,
    time: String,
    progress: Number,
    isInstructor: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['editCourse', 'deleteCourse']);

const image = props.thumbnail ? `../../server${props.thumbnail}` : '../../src/assets/resource_placeholder.png';

const handleEditClick = (event) => {
    event.preventDefault(); // Prevent navigation from router-link
    emit('editCourse', props.courseId);
};

const handleDeleteClick = (event) => {
    event.preventDefault(); // Prevent navigation from router-link
    emit('deleteCourse', props.courseId);
};
</script>
<template>
    <router-link :to="{'name': 'Course', params: { id: courseId }}">
    <div class="flex w-auto h-25 rounded-[12px] justify-between px-15 items-center bg-(--md-sys-color-surface)">
        
        <div class="flex flex-1 justify-center items-center gap-2">
            <img :src="image" class="w-15 h-15 rounded-full" alt="">
            <div class="flex flex-col">
                <span class="text-(length:--md-sys-typescale-title-medium-font)">{{ courseName }}</span>
                <span class="text-(length:--md-sys-typescale-body-small-font)">{{ description }}</span>
            </div>
        </div>
        <div class="flex-1 text-center">
            <span>{{time}}</span>
        </div>

        <div class="flex flex-1 justify-center">
            <md-linear-progress :value="progress" class="w-75"></md-linear-progress>
        </div>
        
        <div v-if="isInstructor" class="ml-4 mr-2 flex">
            <md-icon-button @click="handleEditClick">
                <md-icon>edit</md-icon>
            </md-icon-button>
            <md-icon-button @click="handleDeleteClick">
                <md-icon>delete</md-icon>
            </md-icon-button>
        </div>
    </div>
    </router-link>
</template>