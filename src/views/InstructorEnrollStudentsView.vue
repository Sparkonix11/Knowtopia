<script setup>
import BaseLayout from '@/components/BaseLayout.vue';
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import { getUserStudents } from '@/services/operations/userAPI';
import { getInstructorCoursesAPI, enrollStudentAPI } from '@/services/operations/courseAPI';

const store = useStore();
const students = ref([]);
const courses = ref([]);
const selectedCourse = ref(null);
const isLoading = ref(false);
const error = ref(null);
const successMessage = ref('');
const searchQuery = ref('');

// Computed property for filtered students based on search query
const filteredStudents = computed(() => {
  if (!searchQuery.value) return students.value;
  const query = searchQuery.value.toLowerCase();
  return students.value.filter(student => 
    student.fname.toLowerCase().includes(query) || 
    student.lname.toLowerCase().includes(query) || 
    student.email.toLowerCase().includes(query)
  );
});

// Fetch students and instructor courses on component mount
onMounted(async () => {
  await fetchStudents();
  await fetchInstructorCourses();
});

// Fetch all students
async function fetchStudents() {
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await getUserStudents();
    if (response.status === 200) {
      students.value = response.data.students;
    } else {
      error.value = response.data.error || 'Failed to fetch students';
    }
  } catch (err) {
    error.value = 'An error occurred while fetching students';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
}

// Fetch instructor courses
async function fetchInstructorCourses() {
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await getInstructorCoursesAPI();
    if (response.status === 200) {
      courses.value = response.data.courses;
      if (courses.value.length > 0) {
        selectedCourse.value = courses.value[0];
      }
    } else {
      error.value = response.data.error || 'Failed to fetch courses';
    }
  } catch (err) {
    error.value = 'An error occurred while fetching courses';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
}

// Enroll a student in the selected course
async function enrollStudent(studentId) {
  if (!selectedCourse.value) {
    error.value = 'Please select a course first';
    return;
  }
  
  isLoading.value = true;
  error.value = null;
  successMessage.value = '';
  
  try {
    const response = await enrollStudentAPI(selectedCourse.value.id, studentId);
    if (response.status === 201) {
      successMessage.value = 'Student enrolled successfully';
      // Refresh the student list after enrollment
      await fetchStudents();
    } else {
      error.value = response.data.error || 'Failed to enroll student';
    }
  } catch (err) {
    error.value = 'An error occurred while enrolling student';
    console.error(err);
  } finally {
    isLoading.value = false;
    // Clear success message after 3 seconds
    if (successMessage.value) {
      setTimeout(() => {
        successMessage.value = '';
      }, 3000);
    }
  }
}
</script>

<template>
  <BaseLayout contentClass="my-10">
    <div class="w-[90%] px-6 py-3">
      <span class="text-4xl">Enroll Students</span>
    </div>
    
    <!-- Course selection -->
    <div class="w-[90%] p-6 bg-(--md-sys-color-surface) rounded-[12px] mb-4">
      <div class="mb-4">
        <label class="block text-lg mb-2">Select Course</label>
        <select 
          v-model="selectedCourse" 
          class="w-full p-2 rounded-md bg-(--md-sys-color-surface-container) border border-(--md-sys-color-outline)"
        >
          <option v-for="course in courses" :key="course.id" :value="course">
            {{ course.name }}
          </option>
        </select>
      </div>
    </div>
    
    <!-- Student search and list -->
    <div class="w-[90%] p-6 bg-(--md-sys-color-secondary-container) rounded-[12px]">
      <!-- Loading and error states -->
      <div v-if="isLoading" class="text-center py-4">
        Loading...
      </div>
      
      <div v-else-if="error" class="text-center py-4 text-red-500">
        {{ error }}
        <md-filled-button class="mt-4" @click="fetchStudents">Retry</md-filled-button>
      </div>
      
      <div v-else>
        <!-- Success message -->
        <div v-if="successMessage" class="mb-4 p-2 bg-green-100 text-green-800 rounded-md">
          {{ successMessage }}
        </div>
        
        <!-- Search input -->
        <div class="mb-4">
          <label class="block text-lg mb-2">Search Students</label>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search by name or email" 
            class="w-full p-2 rounded-md bg-(--md-sys-color-surface-container) border border-(--md-sys-color-outline)"
          >
        </div>
        
        <!-- Students table -->
        <div class="overflow-x-auto">
          <table class="w-full border-collapse">
            <thead>
              <tr class="bg-(--md-sys-color-surface) text-left">
                <th class="p-3 rounded-tl-md">Name</th>
                <th class="p-3">Email</th>
                <th class="p-3 rounded-tr-md">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="student in filteredStudents" 
                :key="student.id"
                class="border-b border-(--md-sys-color-outline-variant) hover:bg-(--md-sys-color-surface-variant)"
              >
                <td class="p-3">{{ student.fname }} {{ student.lname }}</td>
                <td class="p-3">{{ student.email }}</td>
                <td class="p-3">
                  <md-filled-button 
                    @click="enrollStudent(student.id)"
                    :disabled="isLoading"
                    class="w-24 h-12"
                  >
                    Enroll
                  </md-filled-button>
                </td>
              </tr>
              <tr v-if="filteredStudents.length === 0">
                <td colspan="3" class="p-3 text-center">No students found</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>