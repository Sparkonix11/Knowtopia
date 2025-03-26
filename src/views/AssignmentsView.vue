<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import Sidebar from '@/components/Sidebar.vue';
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { apiConnector } from '../services/apiConnector';
import { assignmentEndpoints, courseEndpoints } from '../services/apis';

const router = useRouter();
const store = useStore();
const user = computed(() => store.getters["user/currentUser"]);

const assignments = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Fetch assignments based on user role
onMounted(async () => {
  try {
    isLoading.value = true;
    error.value = null;
    
    if (user.value.is_instructor) {
      // For instructors, fetch all assignments they created
      await fetchInstructorAssignments();
    } else {
      // For students, fetch assignments from enrolled courses
      await fetchStudentAssignments();
    }
  } catch (err) {
    console.error('Error fetching assignments:', err);
    error.value = err.message || 'Failed to load assignments';
  } finally {
    isLoading.value = false;
  }
});

// Fetch assignments for instructors
const fetchInstructorAssignments = async () => {
  try {
    // First get all courses created by the instructor
    const coursesResponse = await apiConnector('GET', courseEndpoints.INSTRUCTOR_COURSES);
    
    if (coursesResponse.status !== 200) {
      throw new Error(coursesResponse.data?.error || 'Failed to fetch instructor courses');
    }
    
    const instructorCourses = coursesResponse.data.courses;
    const allAssignments = [];
    
    // For each course, get all weeks and their assignments
    for (const course of instructorCourses) {
      const courseResponse = await apiConnector('GET', courseEndpoints.SINGLE_COURSE(course.id));
      
      if (courseResponse.status === 200) {
        const courseData = courseResponse.data.course;
        
        // Process each week to find assignments
        for (const week of courseData.weeks) {
          // Find materials that are assignments
          const weekAssignments = week.materials.filter(material => material.isAssignment);
          
          // Add course and week info to each assignment
          weekAssignments.forEach(assignment => {
            allAssignments.push({
              id: assignment.assignment_id,
              name: assignment.material_name,
              description: assignment.description || '',
              due_date: assignment.due_date,
              courseId: course.id,
              courseName: course.name,
              weekId: week.id,
              weekName: week.name
            });
          });
        }
      }
    }
    
    assignments.value = allAssignments;
  } catch (err) {
    console.error('Error fetching instructor assignments:', err);
    throw err;
  }
};

// Fetch assignments for students
const fetchStudentAssignments = async () => {
  try {
    // First get all enrolled courses
    const coursesResponse = await apiConnector('GET', courseEndpoints.ENROLLED_COURSES);
    
    if (coursesResponse.status !== 200) {
      throw new Error(coursesResponse.data?.error || 'Failed to fetch enrolled courses');
    }
    
    // The API returns enrolled_courses, not courses
    const enrolledCourses = coursesResponse.data.enrolled_courses || [];
    const allAssignments = [];
    
    // For each course, get all weeks and their assignments
    for (const course of enrolledCourses) {
      const courseResponse = await apiConnector('GET', courseEndpoints.SINGLE_COURSE(course.id));
      
      if (courseResponse.status === 200) {
        const courseData = courseResponse.data.course;
        
        // Process each week to find assignments
        for (const week of courseData.weeks) {
          // Find materials that are assignments
          const weekAssignments = week.materials.filter(material => material.isAssignment);
          
          // Add course and week info to each assignment
          weekAssignments.forEach(assignment => {
            allAssignments.push({
              id: assignment.assignment_id,
              name: assignment.material_name,
              description: assignment.description || '',
              due_date: assignment.due_date,
              courseId: course.id,
              courseName: course.name,
              weekId: week.id,
              weekName: week.name
            });
          });
        }
      }
    }
    
    assignments.value = allAssignments;
  } catch (err) {
    console.error('Error fetching student assignments:', err);
    throw err;
  }
};

// Navigate to the assignment in the course view
const goToAssignment = (assignment) => {
  console.log('Navigating to assignment:', assignment);
  router.push({
    name: 'Course',
    params: { id: assignment.courseId },
    query: { assignmentId: assignment.id }
  });
};
// Format date for display
const formatDueDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });
};
</script>

<template>
  <NavbarMain class="fixed top-0 left-0 right-0 z-20" />
  <div class="flex pt-20">
    <Sidebar class="top-20" />
    <div class="flex-1 p-8 ml-[20%]">
      <h1 class="text-2xl font-bold mb-6">
        {{ user.is_instructor ? 'My Created Assignments' : 'My Assignments' }}
      </h1>
      
      <div v-if="isLoading" class="flex justify-center items-center h-64">
        <md-circular-progress indeterminate></md-circular-progress>
      </div>
      
      <div v-else-if="error" class="p-4 bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) rounded-[12px] mb-4">
        <p>{{ error }}</p>
      </div>
      
      <div v-else-if="assignments.length === 0" class="p-4 bg-(--md-sys-color-secondary-container) text-(--md-sys-color-on-secondary-container) rounded-[12px] mb-4">
        <p>{{ user.is_instructor ? 'You have not created any assignments yet.' : 'You do not have any assignments in your enrolled courses.' }}</p>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="assignment in assignments" 
          :key="assignment.id"
          class="p-4 border border-(--md-sys-color-outline-variant) rounded-[12px] cursor-pointer hover:bg-(--md-sys-color-surface-variant) transition-colors"
          @click="goToAssignment(assignment)"
        >
          <div class="flex items-center mb-2">
            <md-icon class="mr-2">assignment</md-icon>
            <h2 class="text-lg font-semibold">{{ assignment.name }}</h2>
          </div>
          
          <p class="text-sm mb-4 line-clamp-2">{{ assignment.description }}</p>
          
          <div class="flex flex-col text-sm text-(--md-sys-color-on-surface-variant)">
            <div class="flex items-center mb-1">
              <md-icon class="text-sm mr-1">book</md-icon>
              <span>{{ assignment.courseName }}</span>
            </div>
            <div class="flex items-center mb-1">
              <md-icon class="text-sm mr-1">calendar_today</md-icon>
              <span>{{ assignment.weekName }}</span>
            </div>
            <div v-if="assignment.due_date" class="flex items-center">
              <md-icon class="text-sm mr-1">schedule</md-icon>
              <span>Due: {{ formatDueDate(assignment.due_date) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>