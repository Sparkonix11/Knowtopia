<script setup>
import BaseLayout from '@/components/BaseLayout.vue';
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getCourseAPI, getEnrolledCoursesAPI } from '@/services/operations/courseAPI';
import { createEnrollmentRequestAPI, getStudentEnrollmentRequestsAPI } from '@/services/operations/enrollmentRequestAPI';

const route = useRoute();
const router = useRouter();
const courses = ref([]);
const selectedCourseId = ref(null);
const message = ref('');
const isLoading = ref(false);
const error = ref(null);
const successMessage = ref('');
const enrollmentRequests = ref([]);
const showRequestForm = ref(true);
const showRequestHistory = ref(false);

// Computed property to filter out courses that already have pending requests
const availableCourses = computed(() => {
  if (!courses.value || !enrollmentRequests.value) return [];
  
  // Get IDs of courses with pending requests
  const pendingRequestCourseIds = enrollmentRequests.value
    .filter(req => req.status === 'pending')
    .map(req => req.course_id);
  
  // Filter out courses with pending requests
  return courses.value.filter(course => !pendingRequestCourseIds.includes(course.id));
});

// Fetch all available courses and enrollment requests
onMounted(async () => {
  try {
    await Promise.all([
      fetchCourses(),
      fetchEnrollmentRequests()
    ]);
  } catch (err) {
    console.error('Error during initialization:', err);
    error.value = 'Failed to initialize page. Please try again.';
  }
});

async function fetchCourses() {
  isLoading.value = true;
  error.value = null;
  
  try {
    // Get all courses
    const allCoursesResponse = await getCourseAPI();
    if (allCoursesResponse.status !== 200) {
      error.value = allCoursesResponse.data?.error || 'Failed to fetch courses';
      return;
    }
    
    // Get enrolled courses
    const enrolledCoursesResponse = await getEnrolledCoursesAPI();
    if (enrolledCoursesResponse.status !== 200) {
      error.value = enrolledCoursesResponse.data?.error || 'Failed to fetch enrolled courses';
      return;
    }
    
    // Filter out courses where student is already enrolled
    const allCourses = allCoursesResponse.data.courses || [];
    const enrolledCourses = enrolledCoursesResponse.data.enrolled_courses || [];
    const enrolledCourseIds = enrolledCourses.map(course => course.id);
    
    // Set available courses (not enrolled)
    courses.value = allCourses.filter(course => !enrolledCourseIds.includes(course.id));
  } catch (err) {
    error.value = 'An error occurred while fetching available courses';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
}

async function fetchEnrollmentRequests() {
  isLoading.value = true;
  error.value = null;
  
  try {
    const response = await getStudentEnrollmentRequestsAPI();
    if (response.status === 200) {
      enrollmentRequests.value = response.data.enrollment_requests || [];
    } else {
      console.error('Error response:', response);
      error.value = response.data?.error || 'Failed to fetch enrollment requests';
    }
  } catch (err) {
    console.error('Exception during fetch enrollment requests:', err);
    error.value = 'An error occurred while fetching enrollment requests';
  } finally {
    isLoading.value = false;
  }
}

async function submitEnrollmentRequest() {
  if (!selectedCourseId.value) {
    error.value = 'Please select a course';
    return;
  }
  
  isLoading.value = true;
  error.value = null;
  successMessage.value = '';
  
  try {
    const response = await createEnrollmentRequestAPI(selectedCourseId.value, message.value);
    if (response.status === 201) {
      successMessage.value = response.data.message || 'Enrollment request submitted successfully';
      message.value = '';
      selectedCourseId.value = null;
      await fetchEnrollmentRequests();
    } else {
      error.value = response.data.error || 'Failed to submit enrollment request';
    }
  } catch (err) {
    error.value = 'An error occurred while submitting enrollment request';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
}

function toggleView(view) {
  if (view === 'form') {
    showRequestForm.value = true;
    showRequestHistory.value = false;
  } else if (view === 'history') {
    showRequestForm.value = false;
    showRequestHistory.value = true;
  }
}

// Get status badge class based on request status
function getStatusBadgeClass(status) {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'approved':
      return 'bg-green-100 text-green-800';
    case 'rejected':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
}
</script>

<template>
  <BaseLayout contentClass="my-10">
    <div class="w-[90%] px-6 py-3">
      <span class="text-4xl">Course Enrollment Requests</span>
    </div>
    
    <div class="w-[90%] flex space-x-4 mb-6">
      <md-filled-button 
        class="w-40 h-12"
        :class="showRequestForm ? 'bg-(--md-sys-color-primary)' : 'bg-(--md-sys-color-surface-variant)'" 
        @click="toggleView('form')"
      >
        Request Enrollment
      </md-filled-button>
      <md-filled-button 
        class="w-40 h-12"
        :class="showRequestHistory ? 'bg-(--md-sys-color-primary)' : 'bg-(--md-sys-color-surface-variant)'" 
        @click="toggleView('history')"
      >
        View My Requests
      </md-filled-button>
    </div>
    
    <!-- Loading and error states -->
    <div v-if="isLoading" class="w-[90%] p-6 text-center">
      Loading...
    </div>
    
    <div v-else-if="error" class="w-[90%] p-6 text-center text-red-500">
      {{ error }}
    </div>
    
    <div v-else-if="successMessage" class="w-[90%] p-6 text-center text-green-500">
      {{ successMessage }}
    </div>
    
    <!-- Request Enrollment Form -->
    <div v-if="showRequestForm" class="w-[90%] p-6 bg-(--md-sys-color-secondary-container) rounded-[12px] flex flex-col gap-3">
      <h2 class="text-2xl mb-4">Request to Enroll in a Course</h2>
      
      <div class="mb-4">
        <label class="block text-sm font-medium mb-2">Select Course</label>
        <select 
          v-model="selectedCourseId" 
          class="w-full p-2 border border-(--md-sys-color-outline) rounded-md"
        >
          <option value="" disabled selected>Choose a course</option>
          <option v-for="course in availableCourses" :key="course.id" :value="course.id">
            {{ course.name }}
          </option>
          <option v-if="availableCourses.length === 0" disabled>No available courses found</option>
        </select>
      </div>
      
      <div class="mb-4">
        <label class="block text-sm font-medium mb-2">Message (Optional)</label>
        <textarea 
          v-model="message" 
          class="w-full p-2 border border-(--md-sys-color-outline) rounded-md" 
          rows="4" 
          placeholder="Why do you want to enroll in this course?"
        ></textarea>
      </div>
      
      <div class="flex justify-end">
        <md-filled-button class="w-34 h-12" @click="submitEnrollmentRequest" :disabled="isLoading || !selectedCourseId">
          Submit Request
        </md-filled-button>
      </div>
    </div>
    
    <!-- View Enrollment Requests History -->
    <div v-if="showRequestHistory" class="w-[90%] p-6 bg-(--md-sys-color-secondary-container) rounded-[12px] flex flex-col gap-3">
      <h2 class="text-2xl mb-4">My Enrollment Requests</h2>
      
      <div v-if="enrollmentRequests.length === 0" class="text-center py-8">
        You haven't made any enrollment requests yet.
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-(--md-sys-color-outline)">
          <thead>
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Course</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Message</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Status</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Date</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-(--md-sys-color-outline)">
            <tr v-for="request in enrollmentRequests" :key="request.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ request.course_name }}</td>
              <td class="px-6 py-4">
                <div class="max-w-xs truncate">{{ request.message || 'No message' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadgeClass(request.status)}`">
                  {{ request.status.charAt(0).toUpperCase() + request.status.slice(1) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {{ new Date(request.created_at).toLocaleDateString() }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </BaseLayout>
</template>