<script setup>
defineProps({
    question: String,
    options: Array,
    type: String
});

const emit = defineEmits(['select-option']);

const handleOptionSelect = (index) => {
    emit('select-option', index);
};
</script>

<template>
    <div class="w-[80%] h-fit p-12 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto">
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
            <div v-for="option in options" class="flex text-xl gap-4 items-center">
                <md-checkbox :id="option" touch-target="wrapper"></md-checkbox>
                <label :for="option">{{option}}</label>
            </div>
        </div>
    </div>
</template>