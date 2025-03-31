import { ref } from "vue";
import { editWeekAPI, getWeekAPI } from "../services/operations/weekAPI";

export function useEditLecture() {
    const isLoading = ref(false);
    const error = ref(null);

    const fetchLecture = async (lectureId) => {
        isLoading.value = true;
        error.value = null;
        
        try {
            // Use the getWeekAPI operation
            const response = await getWeekAPI(lectureId);
            
            if (!response || response.status !== 200) {
                throw new Error(response?.data?.message || "Failed to fetch lecture details");
            }
            
            return response.data.week;
        } catch (err) {
            error.value = err.message;
            return null;
        } finally {
            isLoading.value = false;
        }
    };

    const editLecture = async (courseId, lectureId, name) => {
        if (!courseId || !lectureId || !name) {
            error.value = "Course ID, Lecture ID, and name are required.";
            return null;
        }

        isLoading.value = true;
        error.value = null;
        
        try {
            const formData = new FormData();
            formData.append("name", name);
            
            const response = await editWeekAPI(courseId, lectureId, formData);
            
            if (!response || response.status !== 200) {
                throw new Error(response?.data?.message || "Failed to update lecture. Please try again.");
            }

            // Return the updated lecture
            return response.data.week;
        } catch (err) {
            error.value = err.message;
            return null;
        } finally {
            isLoading.value = false;
        }
    };
    
    return {
        fetchLecture,
        editLecture,
        isLoading,
        error
    };
}