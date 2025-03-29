<script setup>
import { ref, computed, onMounted } from "vue";
import { useEditSubLecture } from "../handlers/useEditSubLecture";
import { apiConnector } from "../services/apiConnector";

const props = defineProps({
    materialId: {
        type: String,
        required: true
    },
    courseId: {
        type: String,
        required: true
    },
    weekId: {
        type: String,
        required: true
    },
    isOpen: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(["close"]);

const { editSubLecture, isLoading, error } = useEditSubLecture();

const title = ref("");
const description = ref("");
const fileInputRef = ref(null);
const transcriptInputRef = ref(null);
const selectedFile = ref(null);
const selectedTranscript = ref(null);
const filePreviewUrl = ref(null);
const transcriptPreviewUrl = ref(null);
const formErrors = ref({
    title: "",
    file: "",
    transcript: ""
});

// Fetch sublecture data on component mount
onMounted(async () => {
    if (props.materialId) {
        try {
            // Fetch material details
            const response = await apiConnector('GET', `http://127.0.0.1:5000/api/v1/material/${props.materialId}`);
            if (response && response.status === 200) {
                const material = response.data.material;
                title.value = material.title;
                description.value = material.description || "";
                if (material.file_url) {
                    filePreviewUrl.value = material.file_url;
                }
                if (material.transcript_url) {
                    transcriptPreviewUrl.value = material.transcript_url;
                }
            }
        } catch (err) {
            console.error("Error fetching sublecture data:", err);
        }
    }
});

// Form validation
const isFormValid = computed(() => {
    return title.value.trim() !== "" && !formErrors.value.title;
});

const validateTitle = () => {
    if (!title.value.trim()) {
        formErrors.value.title = "Sublecture title is required";
        return false;
    } else if (title.value.length < 3) {
        formErrors.value.title = "Sublecture title must be at least 3 characters";
        return false;
    } else {
        formErrors.value.title = "";
        return true;
    }
};

const updateTitle = (event) => {
    title.value = event.target.value;
    validateTitle();
};

const updateDescription = (event) => {
    description.value = event.target.value;
};

const selectFile = (event) => {
    const file = event.target.files[0];
    if (file) {
        selectedFile.value = file;
        filePreviewUrl.value = URL.createObjectURL(file);
        formErrors.value.file = "";
    }
};

const selectTranscript = (event) => {
    const file = event.target.files[0];
    if (file) {
        selectedTranscript.value = file;
        transcriptPreviewUrl.value = URL.createObjectURL(file);
        formErrors.value.transcript = "";
    }
};

const openFileSelector = () => {
    fileInputRef.value.click();
};

const openTranscriptSelector = () => {
    transcriptInputRef.value.click();
};

const closePopup = () => {
    emit("close");
};

const handleEditSubLecture = async () => {
    // Validate title before submission
    const isTitleValid = validateTitle();
    
    if (isTitleValid) {
        const response = await editSubLecture(
            props.materialId, 
            title.value, 
            description.value, 
            selectedFile.value, 
            selectedTranscript.value
        );
        
        if (response) {
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
                <h2 class="text-xl font-bold">Edit Sublecture</h2>
                <md-icon-button @click="closePopup">
                    <md-icon>close</md-icon>
                </md-icon-button>
            </div>
            
            <div v-if="isLoading" class="flex justify-center items-center h-full">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <div v-else class="flex flex-col gap-8 justify-center items-center py-4">
                <div class="w-full">
                    <md-outlined-text-field 
                        class="w-full" 
                        label="Title" 
                        placeholder="Enter Sublecture Title" 
                        @input="updateTitle" 
                        :value="title"
                        :error="!!formErrors.title"
                    ></md-outlined-text-field>
                    <p v-if="formErrors.title" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.title }}</p>
                </div>
                
                <!-- <div class="w-full">
                    <md-outlined-text-field 
                        class="w-full" 
                        type="textarea" 
                        label="Description (Optional)" 
                        placeholder="Enter Description" 
                        rows="3"  
                        @input="updateDescription" 
                        :value="description"
                    ></md-outlined-text-field>
                </div> -->

                <!-- <div class="flex flex-col items-start gap-2 w-full">
                    <label class="text-gray-700 font-medium">Material File (Optional)</label>
                    <div @click="openFileSelector" class="relative w-full h-75 bg-(--md-sys-color-primary-container) border border-(--md-sys-color-outline) rounded-[16px] flex items-center justify-center cursor-pointer hover:bg-(--md-sys-color-secondary-container) transition-all">
                        <div v-if="filePreviewUrl" class="absolute inset-0 w-full h-full flex items-center justify-center rounded-[16px] p-4">
                            <div class="flex flex-col items-center text-(--md-sys-color-on-primary-container)">
                                <md-icon>description</md-icon>
                                <span class="text-center mt-2">File selected. Click to change.</span>
                            </div>
                        </div>
                        <div v-if="!filePreviewUrl" class="flex flex-col items-center text-(--md-sys-color-on-primary-container)">
                            <md-icon>cloud_upload</md-icon>
                            <span>Upload Material File</span>
                        </div>
                    </div>
                    <input ref="fileInputRef" type="file" class="hidden" @change="selectFile" />
                    <p v-if="formErrors.file" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.file }}</p>
                </div>

                <div class="flex flex-col items-start gap-2 w-full">
                    <label class="text-gray-700 font-medium">Transcript File (Optional)</label>
                    <div @click="openTranscriptSelector" class="relative w-full h-75 bg-(--md-sys-color-primary-container) border border-(--md-sys-color-outline) rounded-[16px] flex items-center justify-center cursor-pointer hover:bg-(--md-sys-color-secondary-container) transition-all">
                        <div v-if="transcriptPreviewUrl" class="absolute inset-0 w-full h-full flex items-center justify-center rounded-[16px] p-4">
                            <div class="flex flex-col items-center text-(--md-sys-color-on-primary-container)">
                                <md-icon>description</md-icon>
                                <span class="text-center mt-2">Transcript selected. Click to change.</span>
                            </div>
                        </div>
                        <div v-if="!transcriptPreviewUrl" class="flex flex-col items-center text-(--md-sys-color-on-primary-container)">
                            <md-icon>cloud_upload</md-icon>
                            <span>Upload Transcript File</span>
                        </div>
                    </div>
                    <input ref="transcriptInputRef" type="file" class="hidden" @change="selectTranscript" />
                    <p v-if="formErrors.transcript" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.transcript }}</p>
                </div> -->

                <div class="flex justify-end w-full gap-2">
                    <md-text-button @click="closePopup">Cancel</md-text-button>
                    <md-filled-button 
                        @click="handleEditSubLecture" 
                        :disabled="isLoading || !isFormValid"
                        class="w-20 h-12"
                    > 
                        {{ isLoading ? "Saving..." : "Save" }}
                    </md-filled-button>
                </div>
                <p v-if="error" class="text-red-500">{{ error }}</p>
            </div>
        </div>
    </div>
</template>