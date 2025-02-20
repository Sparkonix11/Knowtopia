<script setup>
defineProps({
    question: String,
    options: Array,
    type: String
})
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
            <div v-for="option in options" class="flex text-xl gap-4 items-center">
                <md-radio :id="option" :name="question" :value="option"></md-radio>
                <label :for="option">{{option}}</label>
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