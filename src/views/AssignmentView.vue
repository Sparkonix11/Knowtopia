<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import SidebarCourse from '@/components/SidebarCourse.vue';
import QuestionCard from '../components/QuestionCard.vue';
</script>

<template>
    <NavbarMain />
    <div class="flex">
        <SidebarCourse :lectures="lecturedata.lectures"/>
        <div class="flex-1 flex flex-col items-center my-10 gap-6">
            <div v-for="question in questiondata.questions" :key="question.question" class=" w-full">
                <QuestionCard :question="question.question" :options="question.options" :type="question.type" />
            </div>

            <div class="flex justify-end w-[80%]">
                <router-link :to="{'name': 'AssignmentReport'}">
                    <md-filled-button class="w-30 h-14">Submit</md-filled-button>
                </router-link>
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

const questiondata = {
  "questions": [
    {
      "question": "What is the capital of France?",
      "options": ["Berlin", "Madrid", "Paris", "Rome"],
      "type": "MCQ"
    },
    {
      "question": "Which of the following are programming languages?",
      "options": ["Python", "HTML", "Java", "CSS"],
      "type": "MSQ"
    }
  ]
}

</script>