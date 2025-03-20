import { ref, computed, onMounted } from "vue";
import { useStore } from "vuex";

export function useInstructorCourses() {
  const store = useStore();
  
  // Loading and error states
  const isLoading = ref(false);
  const error = ref(null);
  
  // UI state for create views
  const showCreateCourse = ref(false);
  const showCreateLecture = ref(false);
  
  // Get courses from store
  const instructorCourses = computed(() => store.getters["course/getInstructorCourses"]);

  // Toggle UI functions
  const toggleCreateCourse = () => {
    showCreateCourse.value = !showCreateCourse.value;
  };
  
  const toggleCreateLecture = () => {
    showCreateLecture.value = !showCreateLecture.value;
  };
  
  // Fetch instructor courses
  const fetchInstructorCourses = async () => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await store.dispatch("course/updateInstructorCourses");      
      if (response.status !== 200) {
        error.value = response.message || "Failed to fetch instructor courses";
      }
      
      return response;
    } catch (err) {
      error.value = err.message || "An unexpected error occurred";
      return {
        status: 500,
        message: error.value
      };
    } finally {
      isLoading.value = false;
    }
  };
  
  // Fetch courses on component mount
  onMounted(async () => {
    await fetchInstructorCourses();
  });
  
  return {
    // State
    instructorCourses,
    isLoading,
    error,
    showCreateCourse,
    showCreateLecture,
    
    // Methods
    fetchInstructorCourses,
    toggleCreateCourse,
    toggleCreateLecture
  };
}