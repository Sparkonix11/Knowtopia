<script setup>
import NavBarMain from '@/components/NavBarMain.vue';
import SidebarCourse from '@/components/SidebarCourse.vue';
import MinimalSidebarCourse from '@/components/MinimalSidebarCourse.vue';
import placeholder from '@/assets/placeholder.mp4';
import WriteReview from '@/components/WriteReview.vue';
import Summaries from '@/components/Summaries.vue';
import QuestionCard from '@/components/QuestionCard.vue';
import EditLecturePopup from '@/components/EditLecturePopup.vue';
import EditSubLecturePopup from '@/components/EditSubLecturePopup.vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import axios from 'axios';

import { ref, onMounted, computed } from "vue";
import { getInstructorCoursesAPI, getEnrolledCoursesAPI, getSingleCourseAPI } from '@/services/operations/courseAPI';
import { deleteWeekAPI } from '@/services/operations/weekAPI';
import { deleteMaterialAPI } from '@/services/operations/materialAPI';
import { useAssignment } from '@/handlers/useAssignment';
import { apiConnector } from '@/services/apiConnector';
import { questionEndpoints } from '@/services/apis';

const { LIST_QUESTIONS } = questionEndpoints;

const route = useRoute();
const router = useRouter();
const store = useStore();

const showWriteReview = ref(false);
const showSummaries = ref(false);
const showEditLecture = ref(false);
const showEditSubLecture = ref(false);
const isLoading = ref(false);
const error = ref(null);
const courseData = ref(null);
const lectureData = ref({ lectures: [] });
const isInstructor = computed(() => store.getters['user/getUser']?.role === 'instructor');
const currentMaterial = ref(null);
const currentLectureId = ref(null);
const currentSubLectureId = ref(null);
const currentWeekId = ref(null);

// Initialize the assignment handler
const {
  questions,
  selectedAnswers,
  isLoadingQuestions,
  isSubmitting,
  questionError,
  submissionError,
  submissionSuccess,
  submissionResult,
  fetchAssignmentQuestions,
  selectAnswer,
  submitAssignment,
  resetAssignment
} = useAssignment();

// Fetch course data on component mount
onMounted(async () => {
  try {
    isLoading.value = true;
    
    // Check if we have an assignmentId in the query parameters
    const assignmentIdFromQuery = route.query.assignmentId;
    console.log('Assignment ID from query:', assignmentIdFromQuery);
    
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
      
      // Find the current course (use route params if available, otherwise take first course)
      const courseIdFromParams = route.params.id;
      let courseId;
      
      if (courseIdFromParams) {
        // Use the course ID from route params if available
        courseId = courseIdFromParams;
      } else if (courses && courses.length > 0) {
        // Otherwise use the first course
        courseId = courses[0].id;
      } else {
        error.value = 'No courses available';
        isLoading.value = false;
        return;
      }
      
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
                description: material.description,
                type: material.isAssignment ? 'assignment' : (material.type || 'video'),
                url: material.file_path ? `../../server${material.file_path}` : null,
                duration: material.duration,
                isAssignment: material.isAssignment || material.type === 'assignment',
                // Store the assignment ID separately if this is an assignment
                assignment_id: material.isAssignment ? material.assignment_id : null
              };
            }) : []
          }));
          
          // If we have an assignmentId in the query, find and select that assignment
          if (assignmentIdFromQuery) {
            let foundAssignment = false;
            
            // Search through all lectures and materials to find the matching assignment
            for (const lecture of lectureData.value.lectures) {
              for (const material of lecture.subLectures) {
                if (material.isAssignment && material.assignment_id == assignmentIdFromQuery) {
                  // Found the assignment, select it
                  console.log('Found matching assignment:', material);
                  currentMaterial.value = material;
                  foundAssignment = true;
                  
                  // Load the assignment questions
                  await selectMaterial(material);
                  break;
                }
              }
              if (foundAssignment) break;
            }
            
            if (!foundAssignment) {
              console.warn('Assignment not found with ID:', assignmentIdFromQuery);
              // Set first material as current if available
              if (lectureData.value.lectures[0]?.subLectures?.length > 0) {
                currentMaterial.value = lectureData.value.lectures[0].subLectures[0];
              }
            }
          } else {
            // No assignment ID in query, set first material as current if available
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
//         } else {
//           error.value = 'Failed to fetch course data';
//         }
//       } else {
//         error.value = 'No courses available';
//       }
//     } else {
//       error.value = 'Failed to fetch course list';
//     }
//         } else {
//           error.value = 'Failed to fetch course data';
//         }
//       } else {
//         error.value = 'No courses available';
//       }
//     } else {
//       error.value = 'Failed to fetch course list';
//     }
//   } catch (err) {
//     console.error('Error fetching course data:', err);
//     error.value = err.message || 'An error occurred while fetching course data';
//   } finally {
//     isLoading.value = false;
//   }
// });

const selectMaterial = async (material) => {
  console.log('Material selected:', material);
  // Always update the current material regardless of type
  currentMaterial.value = material;
  store.dispatch('chat/setCurrentMaterial', material.id);
  
  // Reset assignment-related state when switching materials
  resetAssignment();
  
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

// Submit assignment handler for CourseView
const handleSubmitAssignment = async () => {
  // Make sure we're using the correct assignment ID
  const assignmentId = currentMaterial.value.assignment_id;
  
  if (!assignmentId) {
    submissionError.value = 'Could not submit: Missing assignment ID';
    return;
  }
  
  await submitAssignment(assignmentId);
};

const toggleWriteReview = () => {
    showWriteReview.value = !showWriteReview.value;
};
const toggleSummaries = () => {
    showSummaries.value = !showSummaries.value;
};

const openEditLecture = (lectureId) => {
    currentLectureId.value = lectureId;
    showEditLecture.value = true;
};

const closeEditLecture = () => {
    showEditLecture.value = false;
    // Refresh course data after editing
    if (courseData.value?.id) {
        getSingleCourseAPI(courseData.value.id).then(response => {
            if (response.status === 200) {
                courseData.value = response.data.course;
                // Update lecture data
                if (courseData.value.weeks && courseData.value.weeks.length > 0) {
                    lectureData.value.lectures = courseData.value.weeks.map(week => ({
                        id: week.id,
                        name: week.name,
                        subLectures: week.materials ? week.materials.map(material => ({
                            id: material.material_id,
                            name: material.material_name,
                            description: material.description,
                            type: material.isAssignment ? 'assignment' : (material.type || 'video'),
                            url: material.file_path ? `../../server${material.file_path}` : null,
                            duration: material.duration,
                            isAssignment: material.isAssignment || material.type === 'assignment',
                            assignment_id: material.isAssignment ? material.assignment_id : null
                        })) : []
                    }));
                }
            }
        });
    }
};

const openEditSubLecture = (materialId, weekId) => {
    currentSubLectureId.value = materialId;
    currentWeekId.value = weekId;
    showEditSubLecture.value = true;
};

const closeEditSubLecture = () => {
    showEditSubLecture.value = false;
    refreshCourseData();
};

// Delete lecture functionality
const deleteLecture = async (lectureId) => {
    if (!courseData.value?.id) return;
    
    isLoading.value = true;
    error.value = null;
    
    try {
        const response = await deleteWeekAPI(courseData.value.id, lectureId);
        
        if (response && response.status === 200) {
            // Refresh course data after successful deletion
            await refreshCourseData();
        } else {
            throw new Error(response?.data?.message || "Failed to delete lecture");
        }
    } catch (err) {
        error.value = err.message || "An error occurred while deleting the lecture";
        console.error("Error deleting lecture:", err);
    } finally {
        isLoading.value = false;
    }
};

// Delete sub-lecture (material) functionality
const deleteSubLecture = async (materialId, weekId) => {
    isLoading.value = true;
    error.value = null;
    
    try {
        const response = await deleteMaterialAPI(materialId);
        
        if (response && response.status === 200) {
            // Refresh course data after successful deletion
            await refreshCourseData();
        } else {
            throw new Error(response?.data?.message || "Failed to delete content");
        }
    } catch (err) {
        error.value = err.message || "An error occurred while deleting the content";
        console.error("Error deleting sub-lecture:", err);
    } finally {
        isLoading.value = false;
    }
};

// Helper function to refresh course data
const refreshCourseData = async () => {
    if (courseData.value?.id) {
        const response = await getSingleCourseAPI(courseData.value.id);
        if (response.status === 200) {
            courseData.value = response.data.course;
            // Update lecture data
            if (courseData.value.weeks && courseData.value.weeks.length > 0) {
                lectureData.value.lectures = courseData.value.weeks.map(week => ({
                    id: week.id,
                    name: week.name,
                    subLectures: week.materials ? week.materials.map(material => ({
                        id: material.material_id,
                        name: material.material_name,
                        description: material.description,
                        type: material.isAssignment ? 'assignment' : (material.type || 'video'),
                        url: material.file_path ? `../../server${material.file_path}` : null,
                        duration: material.duration,
                        isAssignment: material.isAssignment || material.type === 'assignment',
                        assignment_id: material.isAssignment ? material.assignment_id : null
                    })) : []
                }));
            }
        }
    }
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
    <NavBarMain class="fixed top-0 left-0 right-0 z-20" />
    <div class="flex pt-20">
        <!-- Minimal sidebar with icons only -->
        <MinimalSidebarCourse
            :lectures="lectureData.lectures"
            @select-material="selectMaterial"
            class="top-20"
        />
        
        <!-- Sidebar with real lecture data -->
        <SidebarCourse 
            :lectures="lectureData.lectures" 
            :courseName="courseData?.name || 'Course'"
            :courseId="courseData?.id"
            @select-material="selectMaterial"
            @edit-lecture="openEditLecture"
            @edit-sublecture="openEditSubLecture"
            @delete-lecture="deleteLecture"
            @delete-sublecture="deleteSubLecture"
            class="top-20 left-14"
        />
        
        <!-- Main content area -->
        <div class="flex-1 flex flex-col my-10 gap-6 w-full px-6 ml-[calc(20%+3.5rem)]">
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
                                    :questionId="question.id"
                                    @select-option="(optionIndex) => selectAnswer(question.id, optionIndex)"
                                />
                            </div>
                        </div>
                        
                        <!-- Submit button -->
                        <div class="flex justify-center">
                            <md-filled-button 
                                @click="handleSubmitAssignment" 
                                :disabled="isSubmitting || submissionSuccess"
                                class="px-8"
                            >
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

    <WriteReview v-if="showWriteReview" @toggleWriteReview="toggleWriteReview" :materialId="currentMaterial?.id"/>
    <Summaries v-if="showSummaries" @toggleSummaries="toggleSummaries" :materialId="currentMaterial?.id" />
    
    <!-- Edit Lecture Popup -->
    <EditLecturePopup 
        v-if="showEditLecture" 
        :isOpen="showEditLecture"
        :courseId="courseData?.id"
        :lectureId="currentLectureId"
        @close="closeEditLecture"
    />
    
    <!-- Edit SubLecture Popup -->
    <EditSubLecturePopup 
        v-if="showEditSubLecture" 
        :isOpen="showEditSubLecture"
        :courseId="courseData?.id"
        :materialId="currentSubLectureId"
        :weekId="currentWeekId"
        @close="closeEditSubLecture"
    />
    
</template>