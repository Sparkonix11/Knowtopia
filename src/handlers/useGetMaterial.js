import { ref } from "vue";
import { getMaterialAPI } from "../services/operations/materialAPI";

export function useGetMaterial() {
    const isLoading = ref(false);
    const error = ref(null);

    const getMaterial = async (materialId) => {
        if (!materialId) {
            error.value = "Material ID is required.";
            return null;
        }

        isLoading.value = true;
        error.value = null;
        
        try {
            const response = await getMaterialAPI(materialId);
            
            if (!response || response.status !== 200) {
                throw new Error(response?.data?.message || "Failed to fetch material. Please try again.");
            }

            // Return the material
            return response.data.material;
        } catch (err) {
            error.value = err.message;
            return null;
        } finally {
            isLoading.value = false;
        }
    };
    
    return {
        getMaterial,
        isLoading,
        error
    };
}