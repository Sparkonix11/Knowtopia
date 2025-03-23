<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import SidebarCourse from '@/components/SidebarCourse.vue';
import QuestionCard from '../components/QuestionCard.vue';
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const assignmentId = ref(null);
const questions = ref([]);
const isLoading = ref(true);
const error = ref(null);
const selectedAnswers = ref({});
const isSubmitting = ref(false);
const submissionError = ref(null);

// Get assignment ID from route params or query
onMounted(async () => {
  try {
    // Get assignment ID from route params or query
    assignmentId.value = route.query.id || route.params.id;
    console.log('AssignmentView mounted, assignment ID:', assignmentId.value);
    console.log('Route query params:', route.query);
    console.log('Route params:', route.params);
    
    if (!assignmentId.value) {
      error.value = 'Assignment ID is missing';
      isLoading.value = false;
      console.log('Error: Assignment ID is missing');
      return;
    }
    
    // Fetch assignment questions
    const response = await axios.get(`/api/v1/question/${assignmentId.value}`);
    
    if (response.data && response.data.questions) {
      questions.value = response.data.questions.map(q => ({
        id: q.id,
        question: q.description,
        options: [q.option1, q.option2, q.option3, q.option4],
        type: 'MCQ', // Default to MCQ for now
        correctOption: q.correct_option
      }));
    }
    
    isLoading.value = false;
  } catch (err) {
    console.error('Error fetching assignment:', err);
    error.value = err.message || 'Failed to load assignment';
    isLoading.value = false;
  }
});

// Handle answer selection
const selectAnswer = (questionId, optionIndex) => {
  selectedAnswers.value[questionId] = optionIndex;
};

// Submit assignment
const submitAssignment = async () => {
  try {
    isSubmitting.value = true;
    submissionError.value = null;
    
    // Validate that all questions have answers
    const unansweredQuestions = questions.value.filter(q => !selectedAnswers.value[q.id]);
    
    if (unansweredQuestions.length > 0) {
      submissionError.value = `Please answer all questions before submitting. ${unansweredQuestions.length} question(s) remaining.`;
      isSubmitting.value = false;
      return;
    }
    
    // Submit answers to the server
    const response = await axios.post(`/api/v1/assignment/submit/${assignmentId.value}`, {
      answers: selectedAnswers.value
    });
    
    // Navigate to the report page with the score data
    router.push({
      name: 'AssignmentReport',
      query: {
        id: assignmentId.value,
        score: response.data.score.correct,
        total: response.data.score.total,
        percentage: response.data.score.percentage
      }
    });
    
  } catch (err) {
    console.error('Error submitting assignment:', err);
    submissionError.value = err.response?.data?.error || err.message || 'Failed to submit assignment';
    isSubmitting.value = false;
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
                <h1 class="text-2xl font-bold mb-6 w-[80%] mx-auto">Assignment Questions</h1>
                
                <div v-for="question in questions" :key="question.id" class="w-full mb-6">
                    <QuestionCard 
                        :question="question.question" 
                        :options="question.options" 
                        :type="question.type" 
                        @select-option="(index) => selectAnswer(question.id, index + 1)" 
                    />
                </div>
                
                <div v-if="submissionError" class="w-[80%] p-4 mb-4 mx-auto bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) rounded-[12px]">
                    <p>{{ submissionError }}</p>
                </div>
                
                <div class="flex justify-end w-[80%] mx-auto">
                    <md-filled-button 
                        class="w-30 h-14" 
                        @click="submitAssignment" 
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