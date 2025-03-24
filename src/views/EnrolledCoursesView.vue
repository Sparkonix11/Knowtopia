<script setup>
import BaseLayout from '@/components/BaseLayout.vue';
import EnrolledCourseCard from '@/components/EnrolledCourseCard.vue';
import { ref, onMounted } from 'vue';
import { courseEndpoints } from '@/services/apis.js';
const { ENROLLED_COURSES } = courseEndpoints;
import { getEnrolledCoursesAPI } from '@/services/operations/courseAPI';

const courses = ref([]);
const isLoading = ref(false);
const error = ref(null);

onMounted(async () => {
  try {
    isLoading.value = true;
    const response = await getEnrolledCoursesAPI();
    if (response.status === 200) {
      courses.value = response.data.enrolled_courses;
    }
  } catch (err) {
    error.value = err.message;
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
    <BaseLayout contentClass="my-10">
            <div class="w-full px-6 py-3">
                <span class=" text-4xl">Enrolled Courses</span>
            </div>
            
            <!-- Loading and error states -->
            <div v-if="isLoading" class="w-full p-6 text-center">
                Loading courses...
            </div>
            
            <div v-else-if="error" class="w-full p-6 text-center text-red-500">
                {{ error }}
            </div>
            
            <div v-else class="w-full h-138 p-6 bg-(--md-sys-color-secondary-container) rounded-[12px] flex flex-col gap-3">
                <!-- Empty state -->
                <div v-if="!courses || courses.length === 0" class="flex flex-col items-center justify-center py-10 text-center">
                    <p class="text-xl mb-2">No enrolled courses found</p>
                    <p class="text-(--md-sys-color-outline) mb-6">Please ask your instructor to enroll you in their course</p>
                </div>
                
                <!-- Courses list -->
                <template v-else>
                    <div class="flex w-auto h-15 rounded-[12px] justify-between px-15 items-center bg-(--md-sys-color-surface)">
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
                    <EnrolledCourseCard v-for="(course, index) in courses" :key="index"
                        :courseName="course.name"
                        :description="course.description"
                        :thumbnail="course.thumbnail_path"
                        :time="'Not available'"
                        :progress="0"
                    />
                </template>
            </div>
    </BaseLayout>
  </template>