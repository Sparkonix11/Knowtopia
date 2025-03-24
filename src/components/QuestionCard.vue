<script setup>
defineProps({
    question: String,
    options: Array,
    type: String
});

const emit = defineEmits(['select-option']);

const handleOptionSelect = (index) => {
    // Add 1 to convert from 0-based to 1-based indexing
    // This ensures the backend receives the correct option number (1-4 instead of 0-3)
    emit('select-option', index + 1);
};
</script>

<template>
    <div class="w-full h-fit p-8 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto">
        <div class="flex justify-between items-center">
            <div class="w-[90%]">
                <span class="text-xl pr-2">Que.</span>
                <span class="text-xl text-justify">{{question}}</span>
            </div>

            <md-outlined-button class="w-24 h-12">Hint</md-outlined-button>
        </div>

        <div v-if="type == 'MCQ'" class="flex flex-col gap-5 mt-6 ">
            <div v-for="(option, index) in options" :key="index" class="flex text-xl gap-4 items-center">
                <md-radio 
                    :id="`${question}-${index}`" 
                    :name="question" 
                    :value="index" 
                    @change="handleOptionSelect(index)"
                ></md-radio>
                <label :for="`${question}-${index}`">{{option}}</label>
            </div>
        </div>

        <div  v-if="type == 'MSQ'" class="flex flex-col gap-5 mt-6 ">
            <div v-for="(option, index) in options" :key="index" class="flex text-xl gap-4 items-center">
                <md-checkbox :id="`${question}-${index}`" touch-target="wrapper"></md-checkbox>
                <label :for="`${question}-${index}`">{{option}}</label>
            </div>
        </div>
    </div>
</template>