<script setup>
import { ref } from 'vue';
import { getQuestionHintAPI } from '../services/operations/aiAPI';

const props = defineProps({
    question: String,
    options: Array,
    type: String,
    questionId: Number
});

const emit = defineEmits(['select-option']);

const hint = ref('');
const isLoadingHint = ref(false);
const showHint = ref(false);

const handleOptionSelect = (index) => {
    // Add 1 to convert from 0-based to 1-based indexing
    // This ensures the backend receives the correct option number (1-4 instead of 0-3)
    emit('select-option', index + 1);
};

const fetchHint = async () => {
    if (!props.questionId) {
        console.error('Question ID is required to fetch hint');
        return;
    }
    
    isLoadingHint.value = true;
    showHint.value = true;
    
    try {
        const response = await getQuestionHintAPI(props.questionId);
        if (response.status === 200) {
            hint.value = response.data.hint;
        } else {
            hint.value = 'Failed to load hint. Please try again.';
        }
    } catch (error) {
        console.error('Error fetching hint:', error);
        hint.value = 'An error occurred while fetching the hint.';
    } finally {
        isLoadingHint.value = false;
    }
};
</script>

<template>
    <div class="w-full h-fit p-8 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto">
        <div class="flex justify-between items-center">
            <div class="w-[90%]">
                <span class="text-xl pr-2">Que.</span>
                <span class="text-xl text-justify">{{question}}</span>
            </div>

            <md-outlined-button class="w-24 h-12" @click="fetchHint">
                <md-circular-progress v-if="isLoadingHint" indeterminate class="mr-2"></md-circular-progress>
                <span v-else>Hint</span>
            </md-outlined-button>
        </div>

        <div v-if="showHint" class="mt-4 p-3 bg-(--md-sys-color-secondary-container) text-(--md-sys-color-on-secondary-container) rounded-[8px]">
            <p v-if="isLoadingHint">Loading hint...</p>
            <div v-else>
                <h3 class="font-medium mb-1">Hint:</h3>
                <p>{{ hint }}</p>
            </div>
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