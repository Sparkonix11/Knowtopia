import { ref, computed } from "vue";
import { useStore } from "vuex";
import { createMaterialAPI } from "../services/operations/materialAPI";
export function useCreateMaterial() {
    const error = ref(null);
    const store = useStore();
    const isLoading = ref(false);

    const weekId = computed(() => store.getters["course/getCreatingWeek"]).value;

    const createMaterial = async (name, duration, file) => {
        if (!name || !duration) {
            error.value = "Matertial name and duration are required.";
            return;
        }

        isLoading.value = true;
        error.value = null;
        console.log(name, duration, file, weekId);
        try {
            const formData = new FormData();
            formData.append("name", name);
            formData.append("duration", duration);
            if (file) {
                formData.append("file", file);
            }
            
            const response = await createMaterialAPI(weekId, formData);
            
            if (!response || response.status !== 201) {
                throw new Error("Failed to create Material. Please try again.");
            }
            await store.dispatch("course/updateInstructorCourses");
            // Extract the course object from the response
            const createdMaterial = response.data.material;

            // Commit the newly created course to the Vuex store
            
            return createdMaterial;
        } catch (err) {
            error.value = err.message;
        } finally {
            isLoading.value = false;
        }
    };
    
    return {
        createMaterial,
        error,
        isLoading
    };
}
