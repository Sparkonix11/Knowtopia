import { ref } from 'vue';
import { getSingleCourseAPI } from '../services/operations/courseAPI';
import { getWeekAPI } from '../services/operations/weekAPI';

export function useGetCourse() {
    const isLoading = ref(false);
    const error = ref(null);

    // Fetch course details
    const getCourse = async (courseId) => {
        if (!courseId) {
            error.value = "Course ID is required.";
            return null;
        }

        isLoading.value = true;
        error.value = null;
        
        try {
            const response = await getSingleCourseAPI(courseId);
            
            if (!response || response.status !== 200) {
                throw new Error(response?.data?.message || "Failed to fetch course. Please try again.");
            }

            // Return the course
            return response.data.course;
        } catch (err) {
            error.value = err.message;
            return null;
        } finally {
            isLoading.value = false;
        }
    };

    // Fetch lecture (week) details
    const getLecture = async (lectureId) => {
        if (!lectureId) {
            error.value = "Lecture ID is required.";
            return null;
        }

        isLoading.value = true;
        error.value = null;
        
        try {
            const response = await getWeekAPI(lectureId);
            
            if (!response || response.status !== 200) {
                throw new Error(response?.data?.message || "Failed to fetch lecture. Please try again.");
            }

            // Return the lecture
            return response.data.week;
        } catch (err) {
            error.value = err.message;
            return null;
        } finally {
            isLoading.value = false;
        }
    };
    
    return {
        getCourse,
        getLecture,
        isLoading,
        error
    };
}