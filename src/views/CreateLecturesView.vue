<script setup>
import CreateSubLectureView from './CreateSubLectureView.vue';
import CreateLecture from '../components/CreateLecture.vue';
import { ref, computed } from 'vue';
import { useCreateLectures } from '../handlers/useCreateLectures';
import { useStore } from 'vuex';

const store = useStore();

const { creatingCourse, creatingCourseWeeks, updateWeeks } = useCreateLectures();

const lectures = computed(() => creatingCourseWeeks.value);
console.log(lectures);


const emit = defineEmits(["toggleCreateLecture"]);
const toggleCreateLecture = () => {
    emit("toggleCreateLecture");
};

const openLectures = ref({});

const toggleLecture = (name) => {
  openLectures.value[name] = !openLectures.value[name];
};

const showCreateSubLecture = ref(false);
const toggleCreateSubLecture = (weekId) => {
    store.commit('course/SET_CREATING_WEEK', weekId);
    showCreateSubLecture.value = !showCreateSubLecture.value;
    updateWeeks();
};

const showAddLecture = ref(false);
const toggleAddLecture = () => {
    
    showAddLecture.value = !showAddLecture.value;
    updateWeeks();
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
                <div class="w-[60%] mx-auto px-25 p-12 rounded-[12px] bg-(--md-sys-color-surface-container)">
                    <span class="px-10 py-2 block text-2xl">Add Lectures</span>

                    <div v-for="lecture in lectures" :key="lecture.name">
                        <!-- Main lecture header -->
                        <md-list class="rounded-[50px] border-1 border-(--md-sys-color-outline) ">
                        <md-list-item @click="toggleLecture(lecture.name)" class=" cursor-pointer bg-(--md-sys-color-secondary-container) rounded-[100px] border-(--md-sys-color-outline) border-b-1 px-5">
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
                            v-for="subLecture in lecture.materials" 
                            :key="subLecture"
                            class="rounded-[100px] px-15 border-b border-(--md-sys-color-outline-variant)"
                            >
                            <div slot="start">
                                <md-icon>subdirectory_arrow_right</md-icon>
                            </div>
                            <span>{{ subLecture.material_name }}</span>
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
                                <md-outlined-button class="w-35 h-12 m-4" @click="toggleCreateSubLecture(lecture.id)">
                                    <md-icon slot="icon">add</md-icon>Add Lecture
                                </md-outlined-button>
                            </div>

                        </div>
                        
                        </md-list>
                    </div>
                </div>
                <div class="flex justify-end w-[50%] mt-8 gap-5">
                    <md-filled-button class="w-30 h-12" @click="toggleAddLecture"> Add </md-filled-button>
                    <md-filled-button class="w-30 h-12" @click="toggleCreateLecture"> Save </md-filled-button>
                </div>

            </div>
        </div>
    </div>
    <CreateSubLectureView v-if="showCreateSubLecture" @toggleCreateSubLecture="toggleCreateSubLecture" />
    <CreateLecture v-if="showAddLecture" @toggleAddLecture="toggleAddLecture" />

</template>
