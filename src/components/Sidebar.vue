<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
const route = useRoute();
const store = useStore();
const user = computed(() => store.getters["user/currentUser"]);

</script>

<template>
    <div class="w-90 h-[calc(100vh-5rem)] bg-(--md-sys-color-surface-container-low) px-3 left-0">
        <div class="h-14 w-full flex items-center px-5">
            <span class="text-(length:--md-sys-typescale-title-medium-font)">  {{ (user?.is_instructor) ? 'Instructor Portal' : 'Student Portal' }}
            </span>

            
        </div>
        <router-link :to="(route.name === 'EnrolledCourses') ? { name: 'StudentDashboard' } : { name: 'InstructorDashboard' }">
            <div :class="['h-14 rounded-[100px] flex items-center gap-2 px-4', (route.name === 'StudentDashboard' || route.name === 'InstructorDashboard')?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
                <md-icon>dashboard</md-icon>
                <span>Dashboard</span>
            </div>
        </router-link>

        <router-link :to="(route.name === 'StudentDashboard') ? { name: 'EnrolledCourses' } : { name: 'InstructorCourses' }">
        <div :class="['h-14 rounded-[100px] flex items-center gap-2 px-4', (route.name === 'EnrolledCourses' || route.name === 'InstructorCourses')?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
            <md-icon>book</md-icon>
            <span>My Courses</span>
        </div>
        </router-link>
        <!-- <div :class="['h-14 rounded-[100px] flex items-center gap-2 px-4', route.name === 'StudyMaterial'?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
            <md-icon>menu_book</md-icon>
            <span>Study Material</span>
        </div> -->
        <router-link :to="{ name: 'Assignment' }">
        <div :class="['h-14 rounded-[100px] flex items-center gap-2 px-4', route.name === 'Assignmets'?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
            <md-icon>two_pager</md-icon>
            <span>Assignments</span>
        </div>
        </router-link>
        
        <router-link v-if="user?.is_instructor" :to="{ name: 'InstructorEnroll' }">
        <div :class="['h-14 rounded-[100px] flex items-center gap-2 px-4', route.name === 'InstructorEnroll'?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
            <md-icon>person_add</md-icon>
            <span>Enroll Students</span>
        </div>
        </router-link>
        
        <router-link v-if="user?.is_instructor" :to="{ name: 'CreateAssignment' }">
        <div :class="['h-14 rounded-[100px] flex items-center gap-2 px-4', route.name === 'CreateAssignment'?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
            <md-icon>assignment_add</md-icon>
            <span>Create Assignment</span>
        </div>
        </router-link>
        <!-- <md-divider></md-divider>
        <div class="h-14 w-full flex items-center px-5 ">
            <span class="text-(length:--md-sys-typescale-title-medium-font)">Saved</span>
        </div>
        <div class="h-14 rounded-[100px] flex items-center gap-2 px-4 hover:bg-(--md-sys-color-on-surface2)">
            <md-icon>book_2</md-icon>
            <span>Notes</span>
        </div> -->
    </div>
   
</template>