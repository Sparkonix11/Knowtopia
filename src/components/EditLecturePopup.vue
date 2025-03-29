<script setup>
import { ref, computed, onMounted } from "vue";
import { useEditCourse } from "../handlers/useEditCourse";
import { apiConnector } from "../services/apiConnector";

const props = defineProps({
    courseId: {
        type: String,
        required: true
    },
    lectureId: {
        type: String,
        required: true
    },
    isOpen: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(["close"]);

const { editCourse, isLoading, error } = useEditCourse();

const name = ref("");
const formErrors = ref({
    name: "",
});

// Fetch lecture data when component is mounted
onMounted(async () => {
    if (props.lectureId) {
        try {
            // Fetch lecture details
            const response = await apiConnector('GET', `http://127.0.0.1:5000/api/v1/week/${props.lectureId}`);
            if (response && response.status === 200) {
                const lecture = response.data.week;
                name.value = lecture.name;
            }
        } catch (err) {
            console.error("Error fetching lecture data:", err);
        }
    }
});

// Form validation
const isFormValid = computed(() => {
    return name.value.trim() !== "" && 
           !formErrors.value.name
});

const validateName = () => {
    if (!name.value.trim()) {
        formErrors.value.name = "Lecture name is required";
        return false;
    } else if (name.value.length < 3) {
        formErrors.value.name = "Lecture name must be at least 3 characters";
        return false;
    } else {
        formErrors.value.name = "";
        return true;
    }
};

const updateName = (event) => {
    name.value = event.target.value;
    validateName();
};

const closePopup = () => {
    emit("close");
};

const handleEditLecture = async () => {
    // Validate all fields before submission
    const isNameValid = validateName();
    
    if (isNameValid) {
        // Update lecture - using FormData instead of JSON
        const formData = new FormData();
        formData.append('name', name.value);
        
        const response = await apiConnector('PUT', `http://127.0.0.1:5000/api/v1/week/edit/${props.courseId}/${props.lectureId}`, formData);
        
        if (response && response.status === 200) {
            // Close the popup and refresh the course data
            closePopup();
        }
    }
};
</script>

<template>
    <div v-if="isOpen" class="fixed inset-0 flex justify-center items-center bg-black/50 z-50">
        <div class="w-[90%] max-w-[600px] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4 overflow-y-auto">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold">Edit Lecture</h2>
                <md-icon-button @click="closePopup">
                    <md-icon>close</md-icon>
                </md-icon-button>
            </div>
            
            <div v-if="isLoading" class="flex justify-center items-center h-full">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <div v-else class="flex flex-col gap-10 justify-center items-center py-4">
                <div class="w-full">
                    <md-outlined-text-field 
                        class="w-full" 
                        label="Name" 
                        placeholder="Enter Lecture Name" 
                        @input="updateName" 
                        :value="name"
                        :error="!!formErrors.name"
                    ></md-outlined-text-field>
                    <p v-if="formErrors.name" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.name }}</p>
                </div>
                

                <div class="flex justify-end w-full gap-2">
                    <md-text-button @click="closePopup">Cancel</md-text-button>
                    <md-filled-button
                        class="w-20 h-12"
                        @click="handleEditLecture" 
                        :disabled="isLoading || !isFormValid"
                    > 
                        {{ isLoading ? "Saving..." : "Save" }}
                    </md-filled-button>
                </div>
                <p v-if="error" class="text-red-500">{{ error }}</p>
            </div>
        </div>
    </div>
</template>