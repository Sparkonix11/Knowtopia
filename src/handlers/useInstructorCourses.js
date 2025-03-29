import { ref, computed, onMounted } from "vue";
import { useStore } from "vuex";
import { deleteCourseAPI } from "../services/operations/courseAPI";

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
  
  // Delete a course
  const deleteCourse = async (courseId) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await deleteCourseAPI(courseId);
      
      if (response.status === 200) {
        // Refresh the courses list after successful deletion
        await fetchInstructorCourses();
        return { success: true, message: "Course deleted successfully" };
      } else {
        error.value = response.data?.message || "Failed to delete course";
        return { success: false, message: error.value };
      }
    } catch (err) {
      error.value = err.message || "An unexpected error occurred";
      return { success: false, message: error.value };
    } finally {
      isLoading.value = false;
    }
  };
  
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
    toggleCreateLecture,
    deleteCourse
  };
}