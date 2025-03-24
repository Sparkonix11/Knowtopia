<script setup>
import NavBarMain from '@/components/NavBarMain.vue';
import SidebarCourse from '@/components/SidebarCourse.vue';
import placeholder from '@/assets/placeholder.mp4';
import WriteReview from '@/components/WriteReview.vue';
import Summaries from '@/components/Summaries.vue';
import QuestionCard from '@/components/QuestionCard.vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import axios from 'axios';

import { ref, onMounted, computed } from "vue";
import { getInstructorCoursesAPI, getEnrolledCoursesAPI, getSingleCourseAPI } from '@/services/operations/courseAPI';
import { submitAssignmentAPI } from '@/services/operations/assignmentAPI';
import { apiConnector } from '@/services/apiConnector';
import { questionEndpoints } from '@/services/apis';

const { LIST_QUESTIONS } = questionEndpoints;

const route = useRoute();
const router = useRouter();
const store = useStore();

const showWriteReview = ref(false);
const showSummaries = ref(false);
const isLoading = ref(false);
const error = ref(null);
const courseData = ref(null);
const lectureData = ref({ lectures: [] });
const isInstructor = computed(() => store.getters['user/getUser']?.role === 'instructor');
const currentMaterial = ref(null);

// Assignment related state variables
const questions = ref([]);
const selectedAnswers = ref({});
const isLoadingQuestions = ref(false);
const questionError = ref(null);
const isSubmitting = ref(false);
const submissionError = ref(null);
const submissionSuccess = ref(false);
const submissionResult = ref(null);

// Fetch course data on component mount
onMounted(async () => {
  try {
    isLoading.value = true;
    
    // First, get a list of courses to find the course ID
    const listResponse = isInstructor.value 
      ? await getInstructorCoursesAPI()
      : await getEnrolledCoursesAPI();
    
    if (listResponse.status === 200) {
      // For instructor, data is in courses
      // For student, data is in enrolled_courses
      const courses = isInstructor.value 
        ? listResponse.data.courses 
        : listResponse.data.enrolled_courses;
      
      // Find the current course (in a real app, you'd use route params)
      // For now, we'll just take the first course if available
      if (courses && courses.length > 0) {
        // Get the course ID
        const courseId = courses[0].id;
        
        // Fetch the specific course with all its data
        const courseResponse = await getSingleCourseAPI(courseId);
        
        if (courseResponse.status === 200) {
          courseData.value = courseResponse.data.course;
          
          // Transform weeks (lectures) data to the format expected by SidebarCourse
          if (courseData.value.weeks && courseData.value.weeks.length > 0) {
            lectureData.value.lectures = courseData.value.weeks.map(week => ({
              id: week.id,
              name: week.name,
              subLectures: week.materials ? week.materials.map(material => {
                // Log material data to debug assignment_id issues
                console.log('Processing material:', material);
                
                return {
                  id: material.material_id,
                  name: material.material_name,
                  type: material.isAssignment ? 'assignment' : (material.type || 'video'),
                  url: material.file_path ? `../../server${material.file_path}` : null,
                  duration: material.duration,
                  isAssignment: material.isAssignment || material.type === 'assignment',
                  // Store the assignment ID separately if this is an assignment
                  assignment_id: material.isAssignment ? material.assignment_id : null
                };
              }) : []
            }));
            
            // Set first material as current if available
            if (lectureData.value.lectures[0]?.subLectures?.length > 0) {
              currentMaterial.value = lectureData.value.lectures[0].subLectures[0];
            }
          }
        } else {
          error.value = 'Failed to fetch course data';
        }
      } else {
        error.value = 'No courses available';
      }
    } else {
      error.value = 'Failed to fetch course list';
    }
  } catch (err) {
    console.error('Error fetching course data:', err);
    error.value = err.message || 'An error occurred while fetching course data';
  } finally {
    isLoading.value = false;
  }
});

const selectMaterial = async (material) => {
  console.log('Material selected:', material);
  // Always update the current material regardless of type
  currentMaterial.value = material;
  
  // Reset assignment-related state when switching materials
  questions.value = [];
  selectedAnswers.value = {};
  submissionError.value = null;
  submissionSuccess.value = false;
  submissionResult.value = null;
  
  // If it's an assignment, fetch the questions
  if (material.isAssignment) {
    console.log('Assignment detected, ID:', material.id);
    // Make sure we're using the correct assignment ID
    const assignmentId = material.assignment_id;
    console.log('Using assignment ID for questions:', assignmentId);
    
    if (assignmentId) {
      await fetchAssignmentQuestions(assignmentId);
    } else {
      console.error('No valid assignment ID found for this material');
      questionError.value = 'Could not load questions: Missing assignment ID';
    }
  }
};

// Fetch assignment questions
const fetchAssignmentQuestions = async (assignmentId) => {
  try {
    isLoadingQuestions.value = true;
    questionError.value = null;
    
    console.log('Fetching questions for assignment ID:', assignmentId);
    const response = await apiConnector('GET', LIST_QUESTIONS(assignmentId));
    console.log('Question API response:', response.data);
    
    if (response.data && response.data.questions) {
      questions.value = response.data.questions.map(q => ({
        id: q.id,
        question: q.question_description || q.description,
        options: [q.option1, q.option2, q.option3, q.option4],
        type: 'MCQ', // Default to MCQ for now
        correctOption: q.correct_option
      }));
      console.log('Processed questions:', questions.value);
    }
  } catch (err) {
    console.error('Error fetching assignment questions:', err);
    questionError.value = err.message || 'Failed to load assignment questions';
  } finally {
    isLoadingQuestions.value = false;
  }
};

// Handle answer selection
const selectAnswer = (questionId, optionIndex) => {
  selectedAnswers.value[questionId] = optionIndex;
};

// Submit assignment
const submitAssignment = async () => {
  try {
    isSubmitting.value = true;
    submissionError.value = null;
    submissionSuccess.value = false;
    
    // Validate that all questions have answers
    const unansweredQuestions = questions.value.filter(q => selectedAnswers.value[q.id] === undefined);
    
    if (unansweredQuestions.length > 0) {
      submissionError.value = `Please answer all questions before submitting. ${unansweredQuestions.length} question(s) remaining.`;
      isSubmitting.value = false;
      return;
    }
    
    // Make sure we're using the correct assignment ID
    const assignmentId = currentMaterial.value.assignment_id;
    
    if (!assignmentId) {
      submissionError.value = 'Could not submit: Missing assignment ID';
      isSubmitting.value = false;
      return;
    }
    
    console.log('Submitting answers for assignment ID:', assignmentId);
    console.log('Answers being submitted:', selectedAnswers.value);
    
    // Submit answers to the server using the API function
    const response = await submitAssignmentAPI(assignmentId, selectedAnswers.value);
    
    if (response.status === 201) {
      // Store the result
      submissionSuccess.value = true;
      submissionResult.value = {
        score: response.data.score.correct,
        total: response.data.score.total,
        percentage: response.data.score.percentage
      };
    } else {
      submissionError.value = response.data?.error || 'Failed to submit assignment';
    }
    
  } catch (err) {
    console.error('Error submitting assignment:', err);
    submissionError.value = err.response?.data?.error || err.message || 'Failed to submit assignment';
  } finally {
    isSubmitting.value = false;
  }
};

const toggleWriteReview = () => {
    showWriteReview.value = !showWriteReview.value;
};
const toggleSummaries = () => {
    showSummaries.value = !showSummaries.value;
};

const getFileType = (url) => {
  if (!url) return null;
  
  // Extract file extension from the URL
  const fileExtension = url.split('.').pop().toLowerCase();
  
  // Return the file type based on extension
  return fileExtension;
};
</script>

<template>
    <NavBarMain />
    <div class="flex">
        <!-- Sidebar with real lecture data -->
        <SidebarCourse 
            :lectures="lectureData.lectures" 
            @select-material="selectMaterial"
        />
        
        <!-- Main content area -->
        <div class="flex-1 flex flex-col items-center my-10 gap-6 w-full px-6">
            <!-- Loading state -->
            <div v-if="isLoading" class="flex justify-center items-center h-[50vh] w-full">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <!-- Error state -->
            <div v-else-if="error" class="flex flex-col items-center justify-center h-[50vh] w-full">
                <div class="bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) p-4 rounded-lg mb-4 w-full">
                    <div class="flex items-center gap-2">
                        <md-icon>error</md-icon>
                        <span>{{ error }}</span>
                    </div>
                </div>
            </div>
            
            <!-- Empty state -->
            <div v-else-if="!currentMaterial" class="flex flex-col items-center justify-center h-[50vh] w-full">
                <p class="text-xl mb-2">No content selected</p>
                <p class="text-(--md-sys-color-outline) mb-6">Please select a lecture from the sidebar</p>
            </div>
            
            <!-- Content display -->
            <template v-else>
                <!-- Video content -->
                <video v-if="getFileType(currentMaterial.url) === 'mp4'" class="w-full rounded-[12px] border border-(--md-sys-color-outline)" controls>
                    <source :src="currentMaterial.url || placeholder" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                
                <!-- PDF content -->
                <iframe v-else-if="getFileType(currentMaterial.url) === 'pdf'" 
                    :src="currentMaterial.url" 
                    class="w-full h-[70vh] rounded-[12px] border border-(--md-sys-color-outline)"
                    frameborder="0">
                </iframe>
                
                <!-- Assignment content -->
                <div v-if="currentMaterial.isAssignment" class="w-full h-[calc(100vh-120px)] rounded-[12px] border border-(--md-sys-color-outline) p-6 overflow-y-auto">
                    <h2 class="text-2xl font-bold mb-4">{{ currentMaterial.name }}</h2>
                    <p class="mb-6">{{ currentMaterial.description || 'No description available for this assignment.' }}</p>
                    
                    <!-- Loading state for questions -->
                    <div v-if="isLoadingQuestions" class="flex justify-center items-center py-8">
                        <md-circular-progress indeterminate></md-circular-progress>
                    </div>
                    
                    <!-- Error state for questions -->
                    <div v-else-if="questionError" class="bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) p-4 rounded-lg mb-4">
                        <div class="flex items-center gap-2">
                            <md-icon>error</md-icon>
                            <span>{{ questionError }}</span>
                        </div>
                    </div>
                    
                    <!-- Questions display -->
                    <div v-else-if="questions.length > 0">
                        <!-- Submission result -->
                        <div v-if="submissionSuccess" class="mb-6 p-4 bg-(--md-sys-color-primary-container) text-(--md-sys-color-on-primary-container) rounded-lg">
                            <h3 class="text-xl font-bold mb-2">Assignment Result</h3>
                            <p>Score: {{ submissionResult.score }} / {{ submissionResult.total }}</p>
                            <p>Percentage: {{ submissionResult.percentage }}%</p>
                        </div>
                        
                        <!-- Submission error -->
                        <div v-if="submissionError" class="mb-6 p-4 bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) rounded-lg">
                            <div class="flex items-center gap-2">
                                <md-icon>error</md-icon>
                                <span>{{ submissionError }}</span>
                            </div>
                        </div>
                        
                        <!-- Questions list -->
                        <div class="flex flex-col gap-6 mb-6">
                            <div v-for="(question, index) in questions" :key="question.id" class="mb-4">
                                <p class="text-lg font-medium mb-2">Question {{ index + 1 }}</p>
                                <QuestionCard 
                                    :question="question.question" 
                                    :options="question.options" 
                                    :type="question.type"
                                    @select-option="(optionIndex) => selectAnswer(question.id, optionIndex)"
                                />
                            </div>
                        </div>
                        
                        <!-- Submit button -->
                        <div class="flex justify-center">
                            <md-filled-button 
                                @click="submitAssignment" 
                                :disabled="isSubmitting || submissionSuccess"
                                class="px-8"
                            >
                                <md-icon v-if="!isSubmitting" class="mr-2">send</md-icon>
                                <md-circular-progress v-if="isSubmitting" indeterminate class="mr-2"></md-circular-progress>
                                {{ isSubmitting ? 'Submitting...' : 'Submit Assignment' }}
                            </md-filled-button>
                        </div>
                    </div>
                    
                    <!-- No questions available -->
                    <div v-else class="text-center py-8">
                        <p class="text-lg">No questions available for this assignment.</p>
                    </div>
                </div>
                
                <!-- Other content types -->
                <div v-else-if="!getFileType(currentMaterial.url)" class="w-full rounded-[12px] border border-(--md-sys-color-outline) flex items-center justify-center h-[50vh]">
                    <p class="text-xl">Content type not supported for preview</p>
                </div>
                
                <!-- Content title and actions -->
                <div class="flex justify-between w-full" v-if="!currentMaterial.isAssignment">
                    <span class="text-3xl">{{ currentMaterial.name }}</span>
                    <div class="flex gap-2">
                        <md-outlined-button class="w-33 h-10" @click="toggleWriteReview">Write Review</md-outlined-button>
                        <md-outlined-button class="w-33 h-10" @click="toggleSummaries">Summarise</md-outlined-button>
                    </div>
                </div>
                
                <!-- Content description -->
                <span class="w-full">
                    {{ currentMaterial.description || 'No description available for this content.' }}
                    <span v-if="currentMaterial.duration">Duration: {{ currentMaterial.duration }} minutes</span>
                </span>
            </template>
        </div>
    </div>

    <WriteReview v-if="showWriteReview" @toggleWriteReview="toggleWriteReview"/>
    <Summaries v-if="showSummaries" @toggleSummaries="toggleSummaries" />
    
</template>