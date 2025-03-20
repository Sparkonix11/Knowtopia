<script setup>
const props = defineProps({
    courseName: String,
    description: String,
    thumbnail: String,
    time: String,
    progress: Number
})
const image = `../../server${props.thumbnail}`;
</script>
<template>
    <router-link :to="{'name': 'Course'}">
    <div class="flex w-auto h-25 rounded-[12px] justify-between px-15 items-center  bg-(--md-sys-color-surface)">
        
        <div class="flex flex-1 justify-center items-center gap-2">
            <img :src="image" class="w-15 h-15 rounded-full" alt="">
            <div class="flex flex-col">
                <span class="text-(length:--md-sys-typescale-title-medium-font)">{{ courseName }}</span>
                <span class="text-(length:--md-sys-typescale-body-small-font)">{{ description }}</span>
            </div>
        </div>
        <div class="flex-1 text-center ">
            <span> {{time}}</span>
        </div>

        <div class="flex flex-1 justify-center">
            <md-linear-progress :value="progress"  class="w-75"></md-linear-progress>
        </div>
    </div>
    </router-link>
</template>