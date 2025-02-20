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

const emit = defineEmits(["toggleCreateSubLecture, toggleCreateLecture"]);

const toggleCreateSubLecture = () => {
    emit("toggleCreateSubLecture");
    emit("toggleCreateLecture");
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
            
            <div class="flex flex-col gap-10 h-full justify-center items-center">
                <div class="flex flex-col items-start gap-2">
                    <label class="text-gray-700 font-medium">Lecture Content</label>
                    <div @click="openFileSelector" class="relative w-200 h-75 bg-(--md-sys-color-primary-container) border border-(--md-sys-color-outline) rounded-[16px] flex items-center justify-center cursor-pointer hover:bg-(--md-sys-color-secondary-container) transition-all">
                        <!-- Image Preview -->
                        <img 
                            v-if="previewUrl" 
                            :src="previewUrl" 
                            alt="File preview" 
                            class="absolute inset-0 w-full h-full object-contain rounded-[16px]"
                        />

                        <!-- Upload Icon & Text (Hidden when image is uploaded) -->
                        <div v-if="!previewUrl" class="flex flex-col items-center text-(--md-sys-color-on-primary-container)">
                            <md-icon>cloud_upload</md-icon>
                            <span>Upload Content</span>
                        </div>
                    </div>
                    <input ref="fileInputRef" type="file" class="hidden" @change="selectFile" />
                </div>
                <md-outlined-text-field class="w-200" label="Title" placeholder="Enter Lecture Title"></md-outlined-text-field>
                <md-outlined-text-field class="w-200" label="Duration" placeholder="Enter Lecture Duration"></md-outlined-text-field>
                <md-outlined-text-field class="w-200" type="textarea" label="Description" placeholder="Enter Lecture Description" rows="3"></md-outlined-text-field>



                <div class="flex justify-end w-200 mt-4"><md-filled-button class="w-30 h-12" @click="toggleCreateSubLecture"> Save </md-filled-button></div>
            </div>
        </div>
    </div>
</template>