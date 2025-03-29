<script setup>
import BaseLayout from '@/components/BaseLayout.vue';
import EnrolledCourseCard from '@/components/EnrolledCourseCard.vue';
import CreateCourseView from './CreateCourseView.vue';
import CreateLecturesView from './CreateLecturesView.vue';
import { useInstructorCourses } from '../handlers/useInstructorCourses';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();

const {
  instructorCourses,
  isLoading,
  error,
  showCreateCourse,
  showCreateLecture,
  fetchInstructorCourses,
  toggleCreateCourse,
  toggleCreateLecture,
  deleteCourse
} = useInstructorCourses();

// Confirmation dialog state
const showDeleteConfirmation = ref(false);
const courseToDelete = ref(null);
const deleteMessage = ref('');

// Function to navigate to edit course page
const navigateToEditCourse = (courseId) => {
  router.push({ name: 'EditCourse', params: { id: courseId } });
};

// Function to show delete confirmation dialog
const confirmDeleteCourse = (courseId) => {
  // Find the course name for better UX in confirmation message
  const course = instructorCourses.value.find(c => c.id === courseId);
  courseToDelete.value = courseId;
  deleteMessage.value = '';
  showDeleteConfirmation.value = true;
};

// Function to handle course deletion
const handleDeleteCourse = async () => {
  if (!courseToDelete.value) return;
  
  const result = await deleteCourse(courseToDelete.value);
  deleteMessage.value = result.message;
  
  if (result.success) {
    // Close the dialog after successful deletion
    setTimeout(() => {
      showDeleteConfirmation.value = false;
      courseToDelete.value = null;
      deleteMessage.value = '';
    }, 1500);
  }
};

// Function to cancel deletion
const cancelDeleteCourse = () => {
  showDeleteConfirmation.value = false;
  courseToDelete.value = null;
  deleteMessage.value = '';
};
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
            
            <div v-else class="w-[90%] p-6 bg-(--md-sys-color-secondary-container) rounded-[12px] flex flex-col gap-3 max-h-[70vh] overflow-y-auto">
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
                        :courseId="course.id"
                        :courseName="course.name" 
                        :description="course.description"
                        :thumbnail="course.thumbnail_path"
                        :time="course.duration || 'N/A'" 
                        :progress="course.progress || 0.6"
                        :isInstructor="true"
                        @editCourse="navigateToEditCourse"
                        @deleteCourse="confirmDeleteCourse"
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
    
    <!-- Delete Confirmation Dialog -->
    <div v-if="showDeleteConfirmation" class="fixed inset-0 bg-transparent bg-opacity-30 backdrop-blur-sm flex items-center justify-center z-50">
        <div class="bg-(--md-sys-color-surface) p-6 rounded-lg shadow-lg max-w-md w-full">
            <h3 class="text-xl font-semibold mb-4">Confirm Deletion</h3>
            <p class="mb-6">Are you sure you want to delete this course? This action cannot be undone.</p>
            
            <div v-if="deleteMessage" class="mb-4 p-2 rounded" :class="{'bg-green-100 text-green-800': deleteMessage.includes('success'), 'bg-red-100 text-red-800': !deleteMessage.includes('success')}">
                {{ deleteMessage }}
            </div>
            
            <div class="flex justify-end gap-3">
                <md-text-button @click="cancelDeleteCourse">Cancel</md-text-button>
                <md-filled-button @click="handleDeleteCourse" class="bg-red-600">Delete</md-filled-button>
            </div>
        </div>
    </div>
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