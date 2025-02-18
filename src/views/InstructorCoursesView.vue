<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import Sidebar from '@/components/Sidebar.vue';
import EnrolledCourseCard from '@/components/EnrolledCourseCard.vue';
import CreateCourseView from './CreateCourseView.vue';
import CreateLecturesView from './CreateLecturesView.vue';

import { ref } from "vue";
const showCreateCourse = ref(false);
const showCreateLecture = ref(false);

const toggleCreateCourse = () => {
    showCreateCourse.value = !showCreateCourse.value;
};
const toggleCreateLecture = () => {
    showCreateLecture.value = !showCreateLecture.value;
};
</script>

<template>
    <NavbarMain />
    <div class="flex">
        <Sidebar />
        <div class="flex-1 flex flex-col items-center my-10 ">
            <div class="w-[90%] px-6 py-3">
                <span class=" text-4xl">My Courses</span>
            </div>
            <div class="w-[90%] h-138 p-6 bg-(--md-sys-color-secondary-container) rounded-[12px] flex flex-col gap-3">
                <div class="flex w-auto h-15 rounded-[12px] justify-between px-15 items-center  bg-(--md-sys-color-surface)">
                    <div class="flex-1 text-center">
                        <span>Name</span>
                    </div>
                    <div class="flex-1 text-center">
                        <span>Time</span>
                    </div>
                    <div class="flex-1 text-center">
                        <span>Progress</span>
                    </div>
                </div>
                <EnrolledCourseCard :courseName="'Name 1'" :description="'Description 1'" :time="'10Hr 52Mins'" :progress="0.6"/>
                <EnrolledCourseCard :courseName="'Name 2'" :description="'Description 2'" :time="'11Hr 45Mins'" :progress="0.3"/>
                <EnrolledCourseCard :courseName="'Name 3'" :description="'Description 3'" :time="'09Hr 14Mins'" :progress="0.5"/>
                <EnrolledCourseCard :courseName="'Name 4'" :description="'Description 4'" :time="'14Hr 32Mins'" :progress="0.8"/>
            </div>

                <div class="flex-1 flex justify-end w-[90%] mt-5"><md-filled-button class="w-30 h-15" @click="toggleCreateCourse"> Add </md-filled-button></div>

        </div>
    </div>
    <CreateCourseView v-if="showCreateCourse" @toggleCreateCourse="toggleCreateCourse"  @toggleCreateLecture="toggleCreateLecture"/>
    <CreateLecturesView v-if="showCreateLecture" :lectures="lecturedata.lectures" @toggleCreateLecture="toggleCreateLecture" />
  </template>
  <script>
const lecturedata = {
    "lectures": [
    {
      "name": "Lecture 1",
      "subLectures": ["Lecture 1.1", "Lecture 1.2", "Lecture 1.3"]
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