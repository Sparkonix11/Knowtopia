import { ref } from "vue";
import { createCourseAPI } from "../services/operations/courseAPI";

export function useCreateCourse() {
    const isLoading = ref(false);
    const error = ref(null);

    const createCourse = async (name, description, file) => {
        if (!name || !description) {
            error.value = "Course name and description are required.";
            return;
        }

        isLoading.value = true;
        error.value = null;
        
        try {
            const formData = new FormData();
            formData.append("name", name);
            formData.append("description", description);
            if (file) {
                formData.append("thumbnail", file);
            }
            
            const response = await createCourseAPI(formData);
            
            if (!response || response.status !== 201) {
                throw new Error("Failed to create course. Please try again.");
            }
            
            return response.data;
        } catch (err) {
            error.value = err.message;
        } finally {
            isLoading.value = false;
        }
    };
    
    return {
        createCourse,
        isLoading,
        error
    };
}
