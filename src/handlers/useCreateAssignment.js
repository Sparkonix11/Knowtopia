import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getInstructorCoursesAPI } from '../services/operations/courseAPI';
import { createAssignmentAPI } from '../services/operations/assignmentAPI';
import { createQuestionAPI } from '../services/operations/questionAPI';

export function useCreateAssignment() {
  const router = useRouter();
  
  // Form state
  const title = ref('');
  const description = ref('');
  const dueDate = ref('');
  const questions = ref([{
    question_description: '',
    option1: '',
    option2: '',
    option3: '',
    option4: '',
    correct_option: '1'
  }]);
  
  // Course and week selection
  const courses = ref([]);
  const selectedCourse = ref(null);
  const weeks = ref([]);
  const selectedWeek = ref(null);
  const isLoadingCourses = ref(false);
  
  // Form validation
  const formErrors = ref({
    title: '',
    description: '',
    dueDate: '',
    questions: [],
    course: '',
    week: ''
  });
  
  // Loading and error states
  const isLoading = ref(false);
  const error = ref(null);
  const success = ref(null);
  
  // Add a new question
  const addQuestion = () => {
    questions.value.push({
      question_description: '',
      option1: '',
      option2: '',
      option3: '',
      option4: '',
      correct_option: '1'
    });
    formErrors.value.questions.push({});
  };
  
  // Remove a question
  const removeQuestion = (index) => {
    if (questions.value.length > 1) {
      questions.value.splice(index, 1);
      formErrors.value.questions.splice(index, 1);
    }
  };
  
  // Validate form
  const validateForm = () => {
    let isValid = true;
    formErrors.value = {
      title: '',
      description: '',
      dueDate: '',
      questions: [],
      course: '',
      week: ''
    };
    
    // Validate course selection
    if (!selectedCourse.value) {
      formErrors.value.course = 'Please select a course';
      isValid = false;
    }
    
    // Validate week selection
    if (!selectedWeek.value) {
      formErrors.value.week = 'Please select a week';
      isValid = false;
    }
  
    // Validate title
    if (!title.value.trim()) {
      formErrors.value.title = 'Assignment title is required';
      isValid = false;
    }
  
    // Validate description
    if (!description.value.trim()) {
      formErrors.value.description = 'Assignment description is required';
      isValid = false;
    }
  
    // Validate questions
    formErrors.value.questions = [];
    questions.value.forEach((q, index) => {
      const questionErrors = {};
      
      if (!q.question_description.trim()) {
        questionErrors.question_description = 'Question is required';
        isValid = false;
      }
      
      if (!q.option1.trim()) {
        questionErrors.option1 = 'Option 1 is required';
        isValid = false;
      }
      
      if (!q.option2.trim()) {
        questionErrors.option2 = 'Option 2 is required';
        isValid = false;
      }
      
      if (!q.option3.trim()) {
        questionErrors.option3 = 'Option 3 is required';
        isValid = false;
      }
      
      if (!q.option4.trim()) {
        questionErrors.option4 = 'Option 4 is required';
        isValid = false;
      }
      
      formErrors.value.questions[index] = questionErrors;
    });
  
    return isValid;
  };
  
  // Fetch instructor courses
  const fetchCourses = async () => {
    isLoadingCourses.value = true;
    try {
      const response = await getInstructorCoursesAPI();
      if (response.status === 200) {
        courses.value = response.data.courses;
      } else {
        error.value = 'Failed to fetch courses';
      }
    } catch (err) {
      error.value = err.message || 'Failed to fetch courses';
    } finally {
      isLoadingCourses.value = false;
    }
  };
  
  // Update weeks when course changes
  watch(selectedCourse, (newCourse) => {
    if (newCourse) {
      weeks.value = newCourse.weeks || [];
      selectedWeek.value = null;
    } else {
      weeks.value = [];
      selectedWeek.value = null;
    }
  });
  
  // Create assignment
  const createAssignment = async () => {
    if (!validateForm()) {
      return false;
    }
  
    isLoading.value = true;
    error.value = null;
    success.value = null;
  
    try {
      // Create assignment
      const formData = new FormData();
      formData.append('name', title.value);
      formData.append('description', description.value);
      if (dueDate.value) {
        formData.append('due_date', dueDate.value);
      }
  
      if (!selectedWeek.value || !selectedWeek.value.id) {
        throw new Error('Please select a valid week');
      }
      
      const response = await createAssignmentAPI(selectedWeek.value.id, formData);
      
      if (response.status !== 201) {
        throw new Error(response.data?.error || 'Failed to create assignment');
      }
      
      const assignmentData = response.data;
      const assignmentId = assignmentData.assignment.id;
  
      // Create questions for the assignment
      console.log(`Creating ${questions.value.length} questions for assignment ID: ${assignmentId}`);
      
      for (let i = 0; i < questions.value.length; i++) {
        const question = questions.value[i];
        console.log(`Creating question ${i+1}/${questions.value.length}:`, question.question_description);
        
        const questionFormData = new FormData();
        questionFormData.append('question_description', question.question_description);
        questionFormData.append('option1', question.option1);
        questionFormData.append('option2', question.option2);
        questionFormData.append('option3', question.option3);
        questionFormData.append('option4', question.option4);
        questionFormData.append('correct_option', question.correct_option);
        
        console.log(`Sending question ${i+1} data to API:`, {
          description: question.question_description,
          options: [question.option1, question.option2, question.option3, question.option4],
          correct: question.correct_option
        });
        
        try {
          const questionResponse = await createQuestionAPI(assignmentId, questionFormData);
          
          console.log(`Question ${i+1} creation response:`, questionResponse);
          
          if (questionResponse.status !== 201) {
            throw new Error(questionResponse.data?.error || 'Failed to create question');
          }
          
          console.log(`Question ${i+1} created successfully with ID: ${questionResponse.data?.question?.id}`);
        } catch (questionErr) {
          console.error(`Error creating question ${i+1}:`, questionErr);
          throw new Error(`Failed to create question ${i+1}: ${questionErr.message}`);
        }
      }
  
      success.value = 'Assignment created successfully!';
      
      // Reset form after successful submission
      title.value = '';
      description.value = '';
      questions.value = [{
        question_description: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: '1'
      }];
      
      return true;
    } catch (err) {
      error.value = err.message;
      return false;
    } finally {
      isLoading.value = false;
    }
  };
  
  return {
    title,
    description,
    dueDate,
    questions,
    formErrors,
    isLoading,
    isLoadingCourses,
    error,
    success,
    courses,
    selectedCourse,
    weeks,
    selectedWeek,
    addQuestion,
    removeQuestion,
    validateForm,
    createAssignment,
    fetchCourses
  };
}