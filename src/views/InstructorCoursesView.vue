<script setup>
import BaseLayout from '@/components/BaseLayout.vue';
import EnrolledCourseCard from '@/components/EnrolledCourseCard.vue';
import CreateCourseView from './CreateCourseView.vue';
import CreateLecturesView from './CreateLecturesView.vue';
import { useInstructorCourses } from '../handlers/useInstructorCourses';


const {
  instructorCourses,
  isLoading,
  error,
  showCreateCourse,
  showCreateLecture,
  fetchInstructorCourses,
  toggleCreateCourse,
  toggleCreateLecture
} = useInstructorCourses();
</script>


<template>
    <BaseLayout contentClass="my-10">
            <div class="w-[90%] px-6 py-3">
                <span class="text-4xl">My Courses</span>
            </div>
            
            <!-- Loading and error states -->
            <div v-if="isLoading" class="w-[90%] p-6 text-center">
                Loading courses...
            </div>
            
            <div v-else-if="error" class="w-[90%] p-6 text-center text-red-500">
                {{ error }}
                <md-filled-button class="mt-4" @click="fetchInstructorCourses">Retry</md-filled-button>
            </div>
            
            <div v-else class="w-[90%] h-138 p-6 bg-(--md-sys-color-secondary-container) rounded-[12px] flex flex-col gap-3">
                <div v-if="instructorCourses && instructorCourses.length > 0" class="flex w-auto h-15 rounded-[12px] justify-between px-15 items-center bg-(--md-sys-color-surface)">
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
                
                <!-- Use actual data from instructorCourses -->
                <template v-if="instructorCourses && instructorCourses.length > 0">
                    <EnrolledCourseCard 
                        v-for="course in instructorCourses" 
                        :key="course.id"
                        :courseName="course.name" 
                        :description="course.description"
                        :thumbnail="course.thumbnail_path"
                        :time="course.duration || 'N/A'" 
                        :progress="course.progress || 0.6"
                    />
                </template>
                
                <!-- Fallback if no courses -->
                <div v-else class="text-center py-8">
                    No courses available. Click "Add" to create your first course.
                </div>
            </div>

            <div class="flex-1 flex justify-end w-[90%] mt-5">
                <md-filled-button class="w-30 h-15" @click="toggleCreateCourse">Add</md-filled-button>
            </div>
    </BaseLayout>
    
    <CreateCourseView 
        v-if="showCreateCourse" 
        @toggleCreateCourse="toggleCreateCourse" 
        @toggleCreateLecture="toggleCreateLecture"
    />
    
    <CreateLecturesView 
        :lectures="lecturedata.lectures"
        v-if="showCreateLecture" 
        @toggleCreateLecture="toggleCreateLecture" 
    />
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