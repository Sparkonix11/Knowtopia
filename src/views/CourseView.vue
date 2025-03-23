<script setup>
import NavBarMain from '@/components/NavBarMain.vue';
import SidebarCourse from '@/components/SidebarCourse.vue';
import placeholder from '@/assets/placeholder.mp4';
import WriteReview from '@/components/WriteReview.vue';
import Summaries from '@/components/Summaries.vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';

import { ref, onMounted, computed } from "vue";
import { getInstructorCoursesAPI, getEnrolledCoursesAPI, getSingleCourseAPI } from '@/services/operations/courseAPI';

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
              subLectures: week.materials ? week.materials.map(material => ({
                id: material.material_id,
                name: material.material_name,
                type: material.isAssignment ? 'assignment' : (material.type || 'video'),
                url: material.file_path ? `../../server${material.file_path}` : null,
                duration: material.duration,
                isAssignment: material.isAssignment || material.type === 'assignment'
              })) : []
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

const selectMaterial = (material) => {
  console.log('Material selected:', material);
  // Check if the selected material is an assignment
  if (material.isAssignment) {
    console.log('Assignment detected, navigating to Assignment view with ID:', material.id);
    // Navigate to the assignment view with the assignment ID
    router.push({
      name: 'Assignment',
      query: { id: material.id }
    });
    console.log('Router push executed');
  } else {
    // For non-assignment materials, just update the current material
    currentMaterial.value = material;
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
        <div class="flex-1 flex flex-col items-center my-10 gap-6">
            <!-- Loading state -->
            <div v-if="isLoading" class="flex justify-center items-center h-[50vh] w-full">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <!-- Error state -->
            <div v-else-if="error" class="flex flex-col items-center justify-center h-[50vh] w-[80%]">
                <div class="bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) p-4 rounded-lg mb-4 w-full">
                    <div class="flex items-center gap-2">
                        <md-icon>error</md-icon>
                        <span>{{ error }}</span>
                    </div>
                </div>
            </div>
            
            <!-- Empty state -->
            <div v-else-if="!currentMaterial" class="flex flex-col items-center justify-center h-[50vh] w-[80%]">
                <p class="text-xl mb-2">No content selected</p>
                <p class="text-(--md-sys-color-outline) mb-6">Please select a lecture from the sidebar</p>
            </div>
            
            <!-- Content display -->
            <template v-else>
                <!-- Video content -->
                <video v-if="getFileType(currentMaterial.url) === 'mp4'" class="w-[80%] rounded-[12px] border border-(--md-sys-color-outline)" controls>
                    <source :src="currentMaterial.url || placeholder" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                
                <!-- PDF content -->
                <iframe v-else-if="getFileType(currentMaterial.url) === 'pdf'" 
                    :src="currentMaterial.url" 
                    class="w-[80%] h-[50vh] rounded-[12px] border border-(--md-sys-color-outline)"
                    frameborder="0">
                </iframe>
                
                <!-- Other content types -->
                <div v-else class="w-[80%] rounded-[12px] border border-(--md-sys-color-outline) flex items-center justify-center h-[50vh]">
                    <div v-if="currentMaterial.isAssignment" class="flex flex-col items-center gap-4">
                        <p class="text-xl">This is an assignment</p>
                        <md-filled-button @click="selectMaterial(currentMaterial)">
                            <md-icon class="mr-2">assignment</md-icon>
                            Open Assignment
                        </md-filled-button>
                    </div>
                    <p v-else class="text-xl">Content type not supported for preview</p>
                </div>
                
                <!-- Content title and actions -->
                <div class="flex justify-between w-[78%]">
                    <span class="text-3xl">{{ currentMaterial.name }}</span>
                    <div class="flex gap-2">
                        <md-outlined-button class="w-33 h-10" @click="toggleWriteReview">Write Review</md-outlined-button>
                        <md-outlined-button class="w-33 h-10" @click="toggleSummaries">Summarise</md-outlined-button>
                    </div>
                </div>
                
                <!-- Content description -->
                <span class="w-[78%]">
                    {{ currentMaterial.description || 'No description available for this content.' }}
                    <span v-if="currentMaterial.duration">Duration: {{ currentMaterial.duration }} minutes</span>
                </span>
            </template>
        </div>
    </div>

    <WriteReview v-if="showWriteReview" @toggleWriteReview="toggleWriteReview"/>
    <Summaries v-if="showSummaries" @toggleSummaries="toggleSummaries" />
    
</template>