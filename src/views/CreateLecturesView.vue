<script setup>
import { ref } from 'vue';

const props = defineProps({
  lectures: {
    type: Array,
    required: true,
    default: () => []
  }
});

const emit = defineEmits(["toggleCreateLecture"]);
const toggleCreateLecture = () => {
    emit("toggleCreateLecture");
};

const openLectures = ref({});

const toggleLecture = (name) => {
  openLectures.value[name] = !openLectures.value[name];
};
</script>

<template>
     <div class="flex justify-center items-center w-full h-full absolute top-0">
        <div class="w-[90%] h-[92vh] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4 ">
            <div class="flex justify-end">
                <md-icon-button @click="toggleCreateLecture">
                    <md-icon>close</md-icon>
                </md-icon-button>
            </div>
            <div class="flex flex-col items-center justify-center h-full">
                <div class="w-[60%] mx-auto px-25 p-12 rounded-[12px]">
                    <span class="px-10 py-2 block text-2xl">Add Lectures</span>
                    <div v-for="lecture in lectures" :key="lecture.name" class="">
                        <!-- Main lecture header -->
                        <md-list class="rounded-[50px] border-1 border-(--md-sys-color-outline) ">
                        <md-list-item @click="toggleLecture(lecture.name)" class=" cursor-pointer rounded-[100px] border-(--md-sys-color-outline) border-b-1 px-5">
                            <div slot="start">
                                <md-icon>list</md-icon>
                            </div>
                            <span class="font-medium">{{ lecture.name }}</span>
                            <div slot="end" class="flex gap-2 items-center">
                            <md-icon-button>
                                <md-icon>edit</md-icon>
                            </md-icon-button>
                            <md-icon-button>
                                <md-icon>delete</md-icon>
                            </md-icon-button>
                            <span class=" text-xl">|</span>
                            <md-icon>{{ openLectures[lecture.name] ? 'expand_less' : 'expand_more' }}</md-icon>
                            </div>
                        </md-list-item>

                        <!-- Sub lectures dropdown -->
                        <div v-if="openLectures[lecture.name]" class="rounded-[50px]">
                            <md-list-item 
                            v-for="subLecture in lecture.subLectures" 
                            :key="subLecture"
                            class="bg-purple-50/50  rounded-[100px] px-15 border-b border-(--md-sys-color-outline-variant)"
                            >
                            <div slot="start">
                                <md-icon>subdirectory_arrow_right</md-icon>
                            </div>
                            <span>{{ subLecture }}</span>
                            <div slot="end" class="flex gap-2">
                                <md-icon-button>
                                <md-icon>edit</md-icon>
                                </md-icon-button>
                                <md-icon-button>
                                <md-icon>delete</md-icon>
                                </md-icon-button>
                            </div>
                            </md-list-item>
                            <div class="flex justify-end">
                                <md-outlined-button class="w-35 h-12 m-4" @click="null">
                                    <md-icon slot="icon">add</md-icon>Add Lecture
                                </md-outlined-button>
                            </div>

                        </div>
                        
                        </md-list>
                    </div>
                </div>
                <div class="flex justify-end w-[50%]"><md-filled-button class="w-30 h-12" @click="toggleCreateLecture"> Add </md-filled-button></div>
            <</div>
        </div>
    </div>
</template>
