import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { getAssignmentAPI, submitAssignmentAPI, getAssignmentScoreAPI } from '../services/operations/assignmentAPI';
import { listQuestionsAPI } from '../services/operations/questionAPI';

export function useAssignment() {
  const router = useRouter();
  
  // Assignment data
  const assignmentId = ref(null);
  const assignment = ref(null);
  const questions = ref([]);
  const selectedAnswers = ref({});
  
  // Loading and error states
  const isLoading = ref(false);
  const isLoadingQuestions = ref(false);
  const isSubmitting = ref(false);
  const error = ref(null);
  const questionError = ref(null);
  const submissionError = ref(null);
  const submissionSuccess = ref(false);
  const submissionResult = ref(null);
  
  // Fetch assignment details
  const fetchAssignment = async (id) => {
    try {
      isLoading.value = true;
      error.value = null;
      assignmentId.value = id;
      
      console.log('Fetching assignment:', id);
      const response = await getAssignmentAPI(id);
      
      if (response.status === 200) {
        assignment.value = response.data.assignment;
        return response.data.assignment;
      } else {
        error.value = response.data?.error || 'Failed to fetch assignment';
        return null;
      }
    } catch (err) {
      console.error('Error fetching assignment:', err);
      error.value = err.message || 'An error occurred while fetching assignment';
      return null;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Fetch assignment questions
  const fetchAssignmentQuestions = async (id) => {
    try {
      isLoadingQuestions.value = true;
      questionError.value = null;
      
      console.log('Fetching questions for assignment ID:', id);
      const response = await listQuestionsAPI(id);
      
      if (response.status === 200 && response.data && response.data.questions) {
        questions.value = response.data.questions.map(q => ({
          id: q.id,
          question: q.question_description || q.description,
          options: [q.option1, q.option2, q.option3, q.option4],
          type: 'MCQ', // Default to MCQ for now
          correctOption: q.correct_option
        }));
        console.log('Processed questions:', questions.value);
        return questions.value;
      } else {
        questionError.value = response.data?.error || 'Failed to fetch questions';
        return [];
      }
    } catch (err) {
      console.error('Error fetching assignment questions:', err);
      questionError.value = err.message || 'Failed to load assignment questions';
      return [];
    } finally {
      isLoadingQuestions.value = false;
    }
  };
  
  // Handle answer selection
  const selectAnswer = (questionId, optionIndex) => {
    selectedAnswers.value[questionId] = optionIndex;
  };
  
  // Submit assignment
  const submitAssignment = async (id) => {
    try {
      isSubmitting.value = true;
      submissionError.value = null;
      submissionSuccess.value = false;
      
      // Validate that all questions have answers
      const unansweredQuestions = questions.value.filter(q => selectedAnswers.value[q.id] === undefined);
      
      if (unansweredQuestions.length > 0) {
        submissionError.value = `Please answer all questions before submitting. ${unansweredQuestions.length} question(s) remaining.`;
        return null;
      }
      
      console.log('Submitting answers for assignment ID:', id);
      console.log('Answers being submitted:', selectedAnswers.value);
      
      // Submit answers to the server using the API function
      const response = await submitAssignmentAPI(id, selectedAnswers.value);
      
      if (response.status === 201) {
        // Store the result
        submissionSuccess.value = true;
        submissionResult.value = {
          score: response.data.score.correct,
          total: response.data.score.total,
          percentage: response.data.score.percentage
        };
        return submissionResult.value;
      } else {
        submissionError.value = response.data?.error || 'Failed to submit assignment';
        return null;
      }
      
    } catch (err) {
      console.error('Error submitting assignment:', err);
      submissionError.value = err.response?.data?.error || err.message || 'Failed to submit assignment';
      return null;
    } finally {
      isSubmitting.value = false;
    }
  };
  
  // Get assignment score
  const getAssignmentScore = async (id) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      const response = await getAssignmentScoreAPI(id);
      
      if (response.status === 200) {
        submissionResult.value = {
          score: response.data.score.correct,
          total: response.data.score.total,
          percentage: response.data.score.percentage
        };
        submissionSuccess.value = true;
        return submissionResult.value;
      } else {
        error.value = response.data?.error || 'Failed to fetch assignment score';
        return null;
      }
    } catch (err) {
      console.error('Error fetching assignment score:', err);
      error.value = err.message || 'An error occurred while fetching assignment score';
      return null;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Reset assignment state
  const resetAssignment = () => {
    questions.value = [];
    selectedAnswers.value = {};
    submissionError.value = null;
    submissionSuccess.value = false;
    submissionResult.value = null;
    questionError.value = null;
  };
  
  return {
    // State
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
    
    // Methods
    fetchAssignment,
    fetchAssignmentQuestions,
    selectAnswer,
    submitAssignment,
    getAssignmentScore,
    resetAssignment
  };
}