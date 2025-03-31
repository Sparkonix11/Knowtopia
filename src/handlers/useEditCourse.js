import { ref } from 'vue';
import { editCourseAPI } from '../services/operations/courseAPI';

export function useEditCourse() {
  const isLoading = ref(false);
  const error = ref(null);

  const editCourse = async (courseId, name, description, thumbnailFile) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const formData = new FormData();
      formData.append('name', name);
      formData.append('description', description);
      
      if (thumbnailFile) {
        formData.append('thumbnail', thumbnailFile);
      }
      
      const response = await editCourseAPI(courseId, formData);
      
      if (response.status === 200) {
        return response.data;
      } else {
        error.value = response.message || 'Failed to update course';
        return null;
      }
    } catch (err) {
      error.value = err.message || 'An unexpected error occurred';
      return null;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    editCourse,
    isLoading,
    error
  };
}