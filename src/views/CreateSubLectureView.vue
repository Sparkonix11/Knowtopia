<script setup>
import { ref, computed } from "vue";
import { useCreateMaterial } from "../handlers/useCreateSubLecture";

const { createMaterial, error: apiError, isLoading } = useCreateMaterial();

const name = ref("");
const duration = ref("");
const selectedFile = ref(null);
const fileInputRef = ref(null);
const previewUrl = ref(null);
const fileType = ref("");
const formErrors = ref({
    name: "",
    duration: "",
    file: ""
});

// Form validation
const isFormValid = computed(() => {
    return name.value.trim() !== "" && 
           duration.value.trim() !== "" && 
           selectedFile.value && 
           !formErrors.value.name && 
           !formErrors.value.duration && 
           !formErrors.value.file;
});

const validateName = () => {
    if (!name.value.trim()) {
        formErrors.value.name = "Lecture title is required";
        return false;
    } else if (name.value.length < 3) {
        formErrors.value.name = "Title must be at least 3 characters";
        return false;
    } else {
        formErrors.value.name = "";
        return true;
    }
};

const validateDuration = () => {
    if (!duration.value.trim()) {
        formErrors.value.duration = "Duration is required";
        return false;
    } else if (isNaN(duration.value) || parseInt(duration.value) <= 0) {
        formErrors.value.duration = "Duration must be a positive number";
        return false;
    } else {
        formErrors.value.duration = "";
        return true;
    }
};

const updateName = (event) => {
    name.value = event.target.value;
    validateName();
};

const updateDuration = (event) => {
    duration.value = event.target.value;
    validateDuration();
};

const selectFile = (event) => {
    const file = event.target.files[0];

    if (file) {
        selectedFile.value = file;
        fileType.value = file.type;
        
        // Create a preview URL based on file type
        if (file.type.startsWith("image/")) {
            previewUrl.value = URL.createObjectURL(file);
        } else if (file.type.startsWith("video/")) {
            previewUrl.value = URL.createObjectURL(file);
        } else if (file.type === "application/pdf") {
            // For PDF files, we'll just show an icon
            previewUrl.value = null;
        } else {
            // For other file types
            previewUrl.value = null;
        }
        
        formErrors.value.file = "";
    }
};

// Trigger file input click
const openFileSelector = () => {
    fileInputRef.value.click();
};

const emit = defineEmits(["toggleCreateSubLecture"]);

const toggleCreateSubLecture = () => {
    emit("toggleCreateSubLecture");
};

const handleCreateMaterial = async () => {
    // Validate all fields before submission
    const isNameValid = validateName();
    const isDurationValid = validateDuration();
    
    if (!selectedFile.value) {
        formErrors.value.file = "Please upload a lecture content file";
        return;
    }

    if (isNameValid && isDurationValid) {
        // Check file size to provide appropriate feedback
        const fileSizeMB = selectedFile.value.size / (1024 * 1024);
        const isLargeFile = fileSizeMB > 10; // Consider files larger than 10MB as large
        
        try {
            const response = await createMaterial(name.value, duration.value, selectedFile.value);
            if (response) {
                toggleCreateSubLecture();
            }
        } catch (err) {
            // Error handling is already done in the useCreateMaterial hook
            console.error("Error creating material:", err);
        }
    }
};
</script>


<template>
    <div class="flex justify-center items-center w-full h-full absolute top-0">
        <div class="w-[90%] h-[92vh] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4">
            <div class="flex justify-end">
                <md-icon-button @click="toggleCreateSubLecture">
                    <md-icon>close</md-icon>
                </md-icon-button>
            </div>
            
            <div class="flex flex-col gap-10 h-full justify-center items-center relative">
                <!-- Loading overlay -->
                <div v-if="isLoading" class="absolute inset-0 bg-transparent bg-opacity-50 flex items-center justify-center z-10 rounded-[12px]">
                    <div class="bg-white p-6 rounded-lg flex flex-col items-center">
                        <md-circular-progress indeterminate class="h-10 w-10 mb-4"></md-circular-progress>
                        <p class="text-lg font-medium">Processing your content...</p>
                        <p class="text-sm text-gray-600 mt-2">This may take a moment for video uploads</p>
                    </div>
                </div>
                <h2 class="text-2xl font-bold mb-4">Add Lecture Content</h2>
                
                <!-- Error message -->
                <div v-if="apiError" class="bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) p-4 rounded-lg w-200 mb-4">
                    <div class="flex items-center gap-2">
                        <md-icon>error</md-icon>
                        <span>{{ apiError }}</span>
                    </div>
                </div>
                
                <div class="flex flex-col items-start gap-2 w-200">
                    <label class="text-gray-700 font-medium">Lecture Content</label>
                    <div @click="openFileSelector" class="relative w-full h-75 bg-(--md-sys-color-primary-container) border border-(--md-sys-color-outline) rounded-[16px] flex items-center justify-center cursor-pointer hover:bg-(--md-sys-color-secondary-container) transition-all">
                        <!-- Image Preview -->
                        <img 
                            v-if="previewUrl && fileType.startsWith('image/')" 
                            :src="previewUrl" 
                            alt="File preview" 
                            class="absolute inset-0 w-full h-full object-contain rounded-[16px]"
                        />
                        
                        <!-- Video Preview -->
                        <video 
                            v-if="previewUrl && fileType.startsWith('video/')" 
                            :src="previewUrl" 
                            controls
                            class="absolute inset-0 w-full h-full object-contain rounded-[16px]"
                        ></video>
                        
                        <!-- PDF or other file type indicator -->
                        <div v-if="selectedFile && !previewUrl" class="flex flex-col items-center text-(--md-sys-color-on-primary-container)">
                            <md-icon class="text-4xl">{{ fileType === 'application/pdf' ? 'picture_as_pdf' : 'insert_drive_file' }}</md-icon>
                            <span class="mt-2">{{ selectedFile.name }}</span>
                            <span class="text-sm">{{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB</span>
                        </div>

                        <!-- Upload Icon & Text (Hidden when file is uploaded) -->
                        <div v-if="!selectedFile" class="flex flex-col items-center text-(--md-sys-color-on-primary-container)">
                            <md-icon>cloud_upload</md-icon>
                            <span>Upload Content</span>
                            <span class="text-sm mt-1">(PDF, Video, Image, etc.)</span>
                        </div>
                    </div>
                    <input ref="fileInputRef" type="file" class="hidden" @change="selectFile" />
                    <p v-if="formErrors.file" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.file }}</p>
                </div>
                
                <div class="w-200">
                    <md-outlined-text-field 
                        class="w-full" 
                        label="Title" 
                        placeholder="Enter Lecture Title" 
                        @input="updateName" 
                        :value="name"
                        :error="!!formErrors.name"
                    ></md-outlined-text-field>
                    <p v-if="formErrors.name" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.name }}</p>
                </div>
                
                <div class="w-200">
                    <md-outlined-text-field 
                        class="w-full" 
                        label="Duration (minutes)" 
                        placeholder="Enter Lecture Duration" 
                        type="number"
                        min="1"
                        @input="updateDuration" 
                        :value="duration"
                        :error="!!formErrors.duration"
                    ></md-outlined-text-field>
                    <p v-if="formErrors.duration" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.duration }}</p>
                </div>

                <div class="flex justify-end w-200 mt-4">
                    <md-filled-button 
                        class="w-40 h-12" 
                        @click="handleCreateMaterial"
                        :disabled="isLoading || !isFormValid"
                    > 
                        <div class="flex items-center gap-2">
                            <md-circular-progress v-if="isLoading" indeterminate class="h-5 w-5"></md-circular-progress>
                            <span>{{ isLoading ? "Uploading Content..." : "Save" }}</span>
                        </div>
                    </md-filled-button>
                </div>
            </div>
        </div>
    </div>
</template>