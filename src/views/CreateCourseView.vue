<script setup>
import { ref, computed } from "vue";
import { useCreateCourse } from "../handlers/useCreateCourse";

const { createCourse, isLoading, error } = useCreateCourse();

const name = ref("");
const description = ref("");
const fileInputRef = ref(null);
const previewUrl = ref(null);
const selectedFile = ref(null);
const formErrors = ref({
    name: "",
    description: "",
    thumbnail: ""
});

// Form validation
const isFormValid = computed(() => {
    return name.value.trim() !== "" && 
           description.value.trim() !== "" && 
           !formErrors.value.name && 
           !formErrors.value.description && 
           !formErrors.value.thumbnail;
});

const validateName = () => {
    if (!name.value.trim()) {
        formErrors.value.name = "Course name is required";
        return false;
    } else if (name.value.length < 3) {
        formErrors.value.name = "Course name must be at least 3 characters";
        return false;
    } else {
        formErrors.value.name = "";
        return true;
    }
};

const validateDescription = () => {
    if (!description.value.trim()) {
        formErrors.value.description = "Description is required";
        return false;
    } else if (description.value.length < 10) {
        formErrors.value.description = "Description must be at least 10 characters";
        return false;
    } else {
        formErrors.value.description = "";
        return true;
    }
};

const updateName = (event) => {
    name.value = event.target.value;
    validateName();
};

const updateDescription = (event) => {
    description.value = event.target.value;
    validateDescription();
};

const selectFile = (event) => {
    const file = event.target.files[0];
    if (file) {
        if (file.type.startsWith("image/")) {
            selectedFile.value = file;
            previewUrl.value = URL.createObjectURL(file);
            formErrors.value.thumbnail = "";
        } else {
            formErrors.value.thumbnail = "Please select an image file";
            event.target.value = null; // Reset file input
        }
    }
};

const openFileSelector = () => {
    fileInputRef.value.click();
};

const emit = defineEmits(["toggleCreateCourse", "toggleCreateLecture"]);

const toggleCreateLecture = () => {
    emit("toggleCreateCourse");
    emit("toggleCreateLecture");
};

const toggleCreateCourse = () => {
    emit("toggleCreateCourse");
};

const handleCreateCourse = async () => {
    // Validate all fields before submission
    const isNameValid = validateName();
    const isDescriptionValid = validateDescription();
    
    if (!selectedFile.value) {
        formErrors.value.thumbnail = "Please upload a course thumbnail";
    }
    
    if (isNameValid && isDescriptionValid && selectedFile.value) {
        const response = await createCourse(name.value, description.value, selectedFile.value);
        if (response) {
            toggleCreateLecture();
        }
    }
};
</script>

<template>
    <div class="flex justify-center items-center w-full h-full absolute top-0">
        <div class="w-[90%] h-[92vh] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4">
            <div class="flex justify-end">
                <md-icon-button @click="toggleCreateCourse">
                    <md-icon>close</md-icon>
                </md-icon-button>
            </div>
            
            <div class="flex flex-col gap-10 h-full justify-center items-center">
                <div class="w-200">
                    <md-outlined-text-field 
                        class="w-full" 
                        label="Name" 
                        placeholder="Enter Course Name" 
                        @input="updateName" 
                        :value="name"
                        :error="!!formErrors.name"
                    ></md-outlined-text-field>
                    <p v-if="formErrors.name" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.name }}</p>
                </div>
                
                <div class="w-200">
                    <md-outlined-text-field 
                        class="w-full" 
                        type="textarea" 
                        label="Description" 
                        placeholder="Enter Description" 
                        rows="3"  
                        @input="updateDescription" 
                        :value="description"
                        :error="!!formErrors.description"
                    ></md-outlined-text-field>
                    <p v-if="formErrors.description" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.description }}</p>
                </div>

                <div class="flex flex-col items-start gap-2 w-200">
                    <label class="text-gray-700 font-medium">Course Thumbnail</label>
                    <div @click="openFileSelector" class="relative w-full h-75 bg-(--md-sys-color-primary-container) border border-(--md-sys-color-outline) rounded-[16px] flex items-center justify-center cursor-pointer hover:bg-(--md-sys-color-secondary-container) transition-all">
                        <img 
                            v-if="previewUrl" 
                            :src="previewUrl" 
                            alt="File preview" 
                            class="absolute inset-0 w-full h-full object-contain rounded-[16px]"
                        />
                        <div v-if="!previewUrl" class="flex flex-col items-center text-(--md-sys-color-on-primary-container)">
                            <md-icon>cloud_upload</md-icon>
                            <span>Upload Thumbnail</span>
                        </div>
                    </div>
                    <input ref="fileInputRef" type="file" class="hidden" @change="selectFile" accept="image/*" />
                    <p v-if="formErrors.thumbnail" class="text-red-500 text-sm mt-1 ml-2">{{ formErrors.thumbnail }}</p>
                </div>
                
                <div class="flex justify-end w-200">
                    <md-filled-button 
                        class="w-30 h-12" 
                        @click="handleCreateCourse" 
                        :disabled="isLoading || !isFormValid"
                    > 
                        {{ isLoading ? "Adding..." : "Add" }}
                    </md-filled-button>
                </div>
                <p v-if="error" class="text-red-500">{{ error }}</p>
            </div>
        </div>
    </div>
</template>
