<script setup>
import { ref } from "vue";
import { useCreateCourse } from "../handlers/useCreateCourse";

const { createCourse, isLoading, error } = useCreateCourse();

const name = ref("");
const description = ref("");
const fileInputRef = ref(null);
const previewUrl = ref(null);
const selectedFile = ref(null);

const updateName = (event) => {
    name.value = event.target.value;
};
const updateDescription = (event) => {
    description.value = event.target.value;
};

const selectFile = (event) => {
    const file = event.target.files[0];
    if (file) {
        selectedFile.value = file;
        if (file.type.startsWith("image/")) {
            previewUrl.value = URL.createObjectURL(file);
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
    const response = await createCourse(name.value, description.value, selectedFile.value);
    if (response) {
        toggleCreateLecture();
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
                <md-outlined-text-field class="w-200" label="Name" placeholder="Enter Course Name" @input="updateName" :value="name"></md-outlined-text-field>
                <md-outlined-text-field class="w-200" type="textarea" label="Description" placeholder="Enter Description" rows="3"  @input="updateDescription" :value="description"></md-outlined-text-field>

                <div class="flex flex-col items-start gap-2">
                    <label class="text-gray-700 font-medium">Course Thumbnail</label>
                    <div @click="openFileSelector" class="relative w-200 h-75 bg-(--md-sys-color-primary-container) border border-(--md-sys-color-outline) rounded-[16px] flex items-center justify-center cursor-pointer hover:bg-(--md-sys-color-secondary-container) transition-all">
                        <img 
                            v-if="previewUrl" 
                            :src="previewUrl" 
                            alt="File preview" 
                            class="absolute inset-0 w-full h-full object-contain rounded-[16px]"
                        />
                        <div v-if="!previewUrl" class="flex flex-col items-center text-(--md-sys-color-on-primary-container)">
                            <md-icon>upload</md-icon>
                            <span>Upload</span>
                        </div>
                    </div>
                    <input ref="fileInputRef" type="file" class="hidden" @change="selectFile" accept="image/*" />
                </div>
                
                <div class="flex justify-end w-200">
                    <md-filled-button class="w-30 h-12" @click="handleCreateCourse" :disabled="isLoading"> 
                        {{ isLoading ? "Adding..." : "Add" }}
                    </md-filled-button>
                </div>
                <p v-if="error" class="text-red-500">{{ error }}</p>
            </div>
        </div>
    </div>
</template>
