<script setup>
import { defineProps, defineEmits, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

const props = defineProps({
  lectures: {
    type: Array,
    required: true,
    default: () => []
  },
  courseName: {
    type: String,
    default: 'Course Name'
  }
});

const emit = defineEmits(['select-material']);
const route = useRoute();
const store = useStore();
const user = computed(() => store.getters["user/currentUser"]);

const openLectures = ref({});

const toggleLecture = (name) => {
  openLectures.value[name] = !openLectures.value[name];
};

const selectMaterial = (material) => {
  emit('select-material', material);
};
</script>

<template>
  <div class="w-14 h-[calc(100vh-5rem)] bg-(--md-sys-color-surface-container-low) flex flex-col items-center py-4 left-0 fixed z-10 top-20 border-r border-(--md-sys-color-outline-variant)">
    <!-- Course icon at the top -->
    <div class="h-12 w-12 rounded-full flex items-center justify-center mb-6 bg-(--md-sys-color-primary-container)">
      <md-icon>school</md-icon>
    </div>
    
    <!-- Navigation buttons matching Sidebar.vue -->
    <router-link :to="{ name: user?.is_instructor ? 'InstructorDashboard' : 'StudentDashboard' }">
      <div :class="['h-10 w-10 rounded-full flex items-center justify-center mb-4 cursor-pointer', (route.name === 'StudentDashboard' || route.name === 'InstructorDashboard')?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
        <md-icon>dashboard</md-icon>
      </div>
    </router-link>

    <router-link :to="{ name: user?.is_instructor ? 'InstructorCourses' : 'EnrolledCourses' }">
      <div :class="['h-10 w-10 rounded-full flex items-center justify-center mb-4 cursor-pointer', (route.name === 'EnrolledCourses' || route.name === 'InstructorCourses')?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
        <md-icon>book</md-icon>
      </div>
    </router-link>

    <router-link :to="{ name: 'Assignments' }">
      <div :class="['h-10 w-10 rounded-full flex items-center justify-center mb-4 cursor-pointer', route.name === 'Assignments'?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
        <md-icon>assignment</md-icon>
      </div>
    </router-link>
    
    <router-link v-if="user?.is_instructor" :to="{ name: 'InstructorEnroll' }">
      <div :class="['h-10 w-10 rounded-full flex items-center justify-center mb-4 cursor-pointer', route.name === 'InstructorEnroll'?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
        <md-icon>person_add</md-icon>
      </div>
    </router-link>
    
    <router-link v-if="user?.is_instructor" :to="{ name: 'CreateAssignment' }">
      <div :class="['h-10 w-10 rounded-full flex items-center justify-center mb-4 cursor-pointer', route.name === 'CreateAssignment'?'bg-(--md-sys-color-secondary-container)': 'hover:bg-(--md-sys-color-on-surface2)']">
        <md-icon>assignment_add</md-icon>
      </div>
    </router-link>
    
    <!-- Lecture icons -->
    <!-- <div class="mt-2 border-t border-(--md-sys-color-outline-variant) pt-4 w-10"></div>
    <div v-for="lecture in lectures" :key="lecture.id || lecture.name" class="mb-4">
      <div 
        @click="toggleLecture(lecture.name)" 
        :class="['h-10 w-10 rounded-full flex items-center justify-center cursor-pointer', 
                openLectures[lecture.name] ? 'bg-(--md-sys-color-secondary-container)' : 'hover:bg-(--md-sys-color-on-surface2)']">
        <md-icon>menu_book</md-icon>
      </div>
    </div> -->
  </div>
</template>