<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useEditCourse } from "../handlers/useEditCourse";
import { useGetCourse } from "../handlers/useGetCourse";
import { editWeekAPI } from "../services/operations/weekAPI";

const route = useRoute();
const router = useRouter();
const courseId = route.params.id;
const lectureId = route.query.lectureId;
const isLecture = route.query.isLecture === 'true';

const { editCourse, isLoading: isEditLoading, error: editError } = useEditCourse();
const { getCourse, getLecture, isLoading: isGetLoading, error: getError } = useGetCourse();

// Force loading to end after timeout
const forceLoadingComplete = ref(false);
const dataFetched = ref(false);

// Modified loading state that includes a force complete override
const isLoading = computed(() => {
    // If we've forced loading to complete, or data is fetched, don't show loading
    if (forceLoadingComplete.value || dataFetched.value) {
        return false;
    }
    return isEditLoading.value || isGetLoading.value;
});

const error = computed(() => editError.value || getError.value);

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

// Set a timeout to force exit loading state after 3 seconds
setTimeout(() => {
    forceLoadingComplete.value = true;
}, 3000);

// Fetch course or lecture data on component mount
onMounted(async () => {
    try {
        if (isLecture && lectureId) {
            // Fetch lecture details using the handler
            const lecture = await getLecture(lectureId);
            
            if (lecture) {
                name.value = lecture.name;
                description.value = lecture.description || "";
                // Lectures don't have thumbnails
                previewUrl.value = null;
                dataFetched.value = true;
            } else {
                throw new Error("Failed to fetch lecture details");
            }
        } else if (courseId) {
            // Fetch course details using the handler
            const course = await getCourse(courseId);
            
            if (course) {
                name.value = course.name;
                description.value = course.description || "";
                // Use the correct property name 'thumbnail_path'
                if (course.thumbnail_path) {
                    previewUrl.value = `../../server${course.thumbnail_path}`;
                }
                dataFetched.value = true; // Mark data as fetched
            } else {
                throw new Error("Failed to fetch course details");
            }
        }
    } catch (err) {
        console.error("Error fetching data:", err);
        // Set error message to prevent infinite loading
        editError.value = err.message || "Error loading course data";
    } finally {
        dataFetched.value = true;
    }
});

// Form validation
const isFormValid = computed(() => {
    return name.value.trim() !== "" && 
           description.value.trim() !== "" && 
           !formErrors.value.name && 
           !formErrors.value.description;
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

const handleEditCourse = async () => {
    // Validate all fields before submission
    const isNameValid = validateName();
    const isDescriptionValid = validateDescription();
    
    if (isNameValid && isDescriptionValid) {
        let response;
        
        if (isLecture && lectureId) {
            // Update lecture - using FormData instead of JSON
            const formData = new FormData();
            formData.append('name', name.value);
            formData.append('description', description.value);
            
            response = await editWeekAPI(courseId, lectureId, formData);
            
            if (response && response.status === 200) {
                // Navigate back to course page
                router.push({ name: 'Course', params: { id: courseId } });
            }
        } else {
            // Update course
            response = await editCourse(courseId, name.value, description.value, selectedFile.value);
            if (response) {
                // Navigate back to instructor courses page
                router.push({ name: 'InstructorCourses' });
            }
        }
    }
};
</script>

<template>
    <div class="flex justify-center items-center w-full h-full absolute top-0">
        <div class="w-[90%] h-[92vh] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4 overflow-y-auto">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold">{{ isLecture ? 'Edit Lecture' : 'Edit Course' }}</h2>
                <md-icon-button @click="() => router.push(isLecture ? { name: 'Course', params: { id: courseId } } : { name: 'InstructorCourses' })">
                    <md-icon>close</md-icon>
                </md-icon-button>
            </div>
            
            <div v-if="isLoading" class="flex justify-center items-center h-full">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <div v-else class="flex flex-col gap-10 h-full justify-center items-center py-4">
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

                <div v-if="!isLecture" class="flex flex-col items-start gap-2 w-200">
                    <label class="text-gray-700 font-medium">Course Thumbnail (Optional)</label>
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
                        @click="handleEditCourse" 
                        :disabled="isLoading || !isFormValid"
                    > 
                        {{ isLoading ? "Updating..." : "Update" }}
                    </md-filled-button>
                </div>
                <p v-if="error" class="text-red-500">{{ error }}</p>
            </div>
        </div>
    </div>
</template>