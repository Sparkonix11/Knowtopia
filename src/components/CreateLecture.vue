<script setup>
import { useAddLecture } from "../handlers/useAddLecture";
import { ref } from "vue";

const { addLecture, isLoading, error } = useAddLecture();

const name = ref("");
const updateName = (event) => {
    name.value = event.target.value;
};





const emit = defineEmits(["toggleCreateLecture"]);

const toggleAddLecture = () => {
    emit("toggleAddLecture");
    emit("toggleCreateLecture");
};

const toggleCreateLecture = () => {
    emit("toggleCreateLecture");
};



const handleAddCourse = async () => {
    const response = await addLecture(name.value);
    if (response) {
        toggleAddLecture();
    }
};
</script>

<template>
    <div class="flex justify-center items-center w-full h-full absolute top-0">
        <div class="w-[90%] h-[92vh] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4">
            <div class="flex justify-end">
                <md-icon-button @click="toggleAddLecture">
                    <md-icon>close</md-icon>
                </md-icon-button>
            </div>
            
            <div class="flex flex-col gap-10 h-full justify-center items-center">
                <md-outlined-text-field class="w-200" label="Name" placeholder="Enter Course Name" @input="updateName" :value="name"></md-outlined-text-field>
                
                <div class="flex justify-end w-200">
                    <md-filled-button class="w-30 h-12" @click="handleAddCourse" :disabled="isLoading"> 
                        {{ isLoading ? "Adding..." : "Add" }}
                    </md-filled-button>
                </div>
                <p v-if="error" class="text-red-500">{{ error }}</p>
            </div>
        </div>
    </div>
</template>
