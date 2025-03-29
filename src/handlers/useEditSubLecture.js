import { ref } from "vue";
import { useStore } from "vuex";
import { editMaterialAPI } from "../services/operations/materialAPI";

export function useEditSubLecture() {
    const isLoading = ref(false);
    const error = ref(null);
    const store = useStore();

    const editSubLecture = async (materialId, title, description, file, transcript) => {
        if (!materialId || !title) {
            error.value = "Material ID and title are required.";
            return;
        }

        isLoading.value = true;
        error.value = null;
        
        try {
            const formData = new FormData();
            formData.append("title", title);
            
            if (description) {
                formData.append("description", description);
            }
            
            if (file) {
                formData.append("file", file);
            }
            
            if (transcript) {
                formData.append("transcript", transcript);
            }
            
            const response = await editMaterialAPI(materialId, formData);
            
            if (!response || response.status !== 200) {
                throw new Error(response?.data?.message || "Failed to update sublecture. Please try again.");
            }

            // Return the updated material
            return response.data.material;
        } catch (err) {
            error.value = err.message;
        } finally {
            isLoading.value = false;
        }
    };
    
    return {
        editSubLecture,
        isLoading,
        error
    };
}