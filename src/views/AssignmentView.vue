<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import SidebarCourse from '@/components/SidebarCourse.vue';
import QuestionCard from '../components/QuestionCard.vue';
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAssignment } from '@/handlers/useAssignment';

const route = useRoute();
const router = useRouter();

// Use the assignment handler
const {
  assignmentId,
  assignment,
  questions,
  selectedAnswers,
  isLoading,
  isLoadingQuestions,
  isSubmitting,
  error,
  questionError,
  submissionError,
  submissionSuccess,
  submissionResult,
  fetchAssignment,
  fetchAssignmentQuestions,
  selectAnswer,
  submitAssignment
} = useAssignment();

// Get assignment ID from route params or query
onMounted(async () => {
  try {
    // Get assignment ID from route params or query
    const id = route.query.id || route.params.id;
    console.log('AssignmentView mounted, assignment ID:', id);
    console.log('Route query params:', route.query);
    console.log('Route params:', route.params);
    
    if (!id) {
      error.value = 'Assignment ID is missing';
      console.log('Error: Assignment ID is missing');
      return;
    }
    
    // Fetch assignment details using the handler
    const assignmentData = await fetchAssignment(id);
    
    if (assignmentData) {
      // Fetch questions for this assignment
      await fetchAssignmentQuestions(id);
    }
  } catch (err) {
    console.error('Error in AssignmentView:', err);
    error.value = err.message || 'An error occurred';
  }
});

// Submit assignment and handle redirection
const handleSubmitAssignment = async () => {
  const result = await submitAssignment(assignmentId.value);
  
  if (result) {
    // Redirect to the report page with score data
    router.push({
      name: 'AssignmentReport',
      query: {
        id: assignmentId.value,
        score: result.score,
        total: result.total,
        percentage: result.percentage
      }
    });
  }
};
</script>

<template>
    <NavbarMain />
    <div class="flex">
        <SidebarCourse :lectures="[]"/>
        <div class="flex-1 flex flex-col items-center my-10 gap-6">
            <div v-if="isLoading" class="flex justify-center items-center h-64">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <div v-else-if="error" class="w-[80%] p-6 bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) rounded-[12px]">
                <p>{{ error }}</p>
            </div>
            
            <div v-else>
                <div class="w-[80%] mx-auto mb-8">
                    <h1 class="text-2xl font-bold mb-4">{{ assignment?.name || 'Assignment' }}</h1>
                    <p class="mb-6">{{ assignment?.description || 'No description available for this assignment.' }}</p>
                </div>
                
                <h2 class="text-xl font-bold mb-6 w-[80%] mx-auto">Assignment Questions</h2>
                
                <div v-for="question in questions" :key="question.id" class="w-full mb-6">
                    <QuestionCard 
                        :question="question.question" 
                        :options="question.options" 
                        :type="question.type" 
                        :questionId="question.id"
                        @select-option="(index) => selectAnswer(question.id, index + 1)" 
                    />
                </div>
                
                <div v-if="submissionError" class="w-[80%] p-4 mb-4 mx-auto bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) rounded-[12px]">
                    <p>{{ submissionError }}</p>
                </div>
                
                <div class="flex justify-end w-[80%] mx-auto">
                    <md-filled-button 
                        class="w-30 h-14" 
                        @click="handleSubmitAssignment" 
                        :disabled="isSubmitting"
                    >
                        <md-circular-progress v-if="isSubmitting" indeterminate class="mr-2"></md-circular-progress>
                        {{ isSubmitting ? 'Submitting...' : 'Submit Assignment' }}
                    </md-filled-button>
                </div>
            </div>
        </div>
    </div>
</template>