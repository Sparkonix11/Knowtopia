<script setup>
import { ref } from "vue";

const fileInputRef = ref(null);
const previewUrl = ref(null);

const selectFile = (event) => {
    const file = event.target.files[0];

    if (file) {
        // Create a URL for the preview if the file is an image
        if (file.type.startsWith("image/")) {
            previewUrl.value = URL.createObjectURL(file);
        }
    }
};

// Trigger file input click
const openFileSelector = () => {
    fileInputRef.value.click();
};

const emit = defineEmits(["toggleCreateCourse", "toggleCreateLecture"]);

const toggleCreateCourse = () => {
    emit("toggleCreateCourse");
};
const toggleCreateLecture = () => {
    emit("toggleCreateCourse");
    emit("toggleCreateLecture");
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
                <md-outlined-text-field class="w-200" label="Name" placeholder="Enter Course Name"></md-outlined-text-field>
                <md-outlined-text-field class="w-200" type="textarea" label="Description" placeholder="Enter Description" rows="3"></md-outlined-text-field>

                <div class="flex flex-col items-start gap-2">
                <label class="text-gray-700 font-medium">Course Thumbnail</label>
                    <div @click="openFileSelector" class="relative w-200 h-75 bg-(--md-sys-color-primary-container) border border-(--md-sys-color-outline) rounded-[16px] flex items-center justify-center cursor-pointer hover:bg-purple-200 transition-all">
                        <!-- Image Preview -->
                        <img 
                            v-if="previewUrl" 
                            :src="previewUrl" 
                            alt="File preview" 
                            class="absolute inset-0 w-full h-full object-contain rounded-[16px]"
                        />

                        <!-- Upload Icon & Text (Hidden when image is uploaded) -->
                        <div v-if="!previewUrl" class="flex flex-col items-center text-purple-600">
                            <md-icon>upload</md-icon>
                            <span>Upload</span>
                        </div>
                    </div>

                    <!-- Hidden File Input -->
                    <input ref="fileInputRef" type="file" class="hidden" @change="selectFile" accept="image/*" />
                </div>
                <div class="flex justify-end w-200"><md-filled-button class="w-30 h-12" @click="toggleCreateLecture"> Add </md-filled-button></div>
            </div>
        </div>
    </div>
</template>