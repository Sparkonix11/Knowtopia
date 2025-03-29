<script setup>
import BaseLayout from '@/components/BaseLayout.vue';
import { ref, onMounted, computed } from 'vue';
import { getInstructorEnrollmentRequestsAPI, processEnrollmentRequestAPI } from '@/services/operations/enrollmentRequestAPI';

const enrollmentRequests = ref([]);
const isLoading = ref(false);
const error = ref(null);
const successMessage = ref('');
const selectedFilter = ref('all'); // all, pending, approved, rejected

// Fetch all enrollment requests for instructor's courses
onMounted(async () => {
  await fetchEnrollmentRequests();
});

async function fetchEnrollmentRequests() {
  isLoading.value = true;
  error.value = null;
  successMessage.value = '';
  
  try {
    const response = await getInstructorEnrollmentRequestsAPI();
    if (response.status === 200) {
      enrollmentRequests.value = response.data.enrollment_requests;
    } else {
      error.value = response.data.error || 'Failed to fetch enrollment requests';
    }
  } catch (err) {
    error.value = 'An error occurred while fetching enrollment requests';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
}

async function handleRequestAction(requestId, action) {
  isLoading.value = true;
  error.value = null;
  successMessage.value = '';
  
  try {
    const response = await processEnrollmentRequestAPI(requestId, action);
    if (response.status === 200) {
      successMessage.value = response.data.message || `Request ${action}d successfully`;
      // Update the local state to reflect the change
      const requestIndex = enrollmentRequests.value.findIndex(req => req.id === requestId);
      if (requestIndex !== -1) {
        enrollmentRequests.value[requestIndex].status = action === 'approve' ? 'approved' : 'rejected';
      }
    } else {
      error.value = response.data.error || `Failed to ${action} enrollment request`;
    }
  } catch (err) {
    error.value = `An error occurred while ${action}ing enrollment request`;
    console.error(err);
  } finally {
    isLoading.value = false;
  }
}

// Filter requests based on selected filter
const filteredRequests = computed(() => {
  if (selectedFilter.value === 'all') {
    return enrollmentRequests.value;
  }
  return enrollmentRequests.value.filter(req => req.status === selectedFilter.value);
});

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
      <span class="text-4xl">Enrollment Requests</span>
    </div>
    
    <!-- Filter controls -->
    <div class="w-[90%] flex space-x-4 mb-6">
      <md-filled-button 
        :class="selectedFilter === 'all' ? 'bg-(--md-sys-color-primary)' : 'bg-(--md-sys-color-surface-variant)'" 
        @click="selectedFilter = 'all'"
        class="w-30 h-12"
      >
        All Requests
      </md-filled-button>
      <md-filled-button 
        :class="selectedFilter === 'pending' ? 'bg-(--md-sys-color-primary)' : 'bg-(--md-sys-color-surface-variant)'" 
        @click="selectedFilter = 'pending'"
        class="w-24 h-12"
      >
        Pending
      </md-filled-button>
      <md-filled-button 
        :class="selectedFilter === 'approved' ? 'bg-(--md-sys-color-primary)' : 'bg-(--md-sys-color-surface-variant)'" 
        @click="selectedFilter = 'approved'"
        class="w-24 h-12"
      >
        Approved
      </md-filled-button>
      <md-filled-button 
        :class="selectedFilter === 'rejected' ? 'bg-(--md-sys-color-primary)' : 'bg-(--md-sys-color-surface-variant)'" 
        @click="selectedFilter = 'rejected'"
        class="w-24 h-12"
      >
        Rejected
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
    
    <!-- Enrollment Requests Table -->
    <div class="w-[90%] p-6 bg-(--md-sys-color-secondary-container) rounded-[12px] flex flex-col gap-3">
      <h2 class="text-2xl mb-4">Manage Enrollment Requests</h2>
      
      <div v-if="filteredRequests.length === 0" class="text-center py-8">
        No enrollment requests found.
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-(--md-sys-color-outline)">
          <thead>
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Student</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Course</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Message</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Status</th>
              <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Date</th>
              <th class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-(--md-sys-color-outline)">
            <tr v-for="request in filteredRequests" :key="request.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div>{{ request.student_name }}</div>
                <div class="text-sm text-(--md-sys-color-outline)">{{ request.student_email }}</div>
              </td>
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
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex space-x-2 justify-center">
                  <md-filled-button 
                    v-if="request.status === 'pending'"
                    class="bg-green-600 w-24 h-12" 
                    @click="handleRequestAction(request.id, 'approve')"
                    :disabled="isLoading"
                  >
                    Approve
                  </md-filled-button>
                  <md-filled-button 
                  
                    v-if="request.status === 'pending'"
                    class="bg-red-600 w-24 h-12" 
                    @click="handleRequestAction(request.id, 'reject')"
                    :disabled="isLoading"
                    
                  >
                    Reject
                  </md-filled-button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </BaseLayout>
</template>