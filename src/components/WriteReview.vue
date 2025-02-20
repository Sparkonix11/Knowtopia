<script setup>
import avatar from '@/assets/avatar.png';
const emit = defineEmits(["toggleWriteReview"]);
const toggleWriteReview = () => {
    emit("toggleWriteReview");
};
</script>

<template>
    <div class="flex justify-center items-center w-full h-full absolute top-0">
        <div class="w-[50%] h-[50vh] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4">
            <div class="flex justify-end">
                <md-icon-button @click="toggleWriteReview">
                    <md-icon>close</md-icon>
                </md-icon-button>
            </div>
            <div class="flex flex-col justify-center items-center h-full gap-8">
                <div class="flex items-center gap-2">
                    <img :src="avatar" alt="" class="w-28 h-28 rounded-full">
                    <div class="flex-col justify-center items-center text-center">
                        <span class=" text-xl">User Name</span>
                        <div class="flex items-center">
                            <span class=" text-3xl">&#9733;</span>
                            <span class=" text-3xl">&#9733;</span>
                            <span class=" text-3xl">&#9733;</span>
                            <span class=" text-3xl">&#9733;</span>
                            <span class=" text-3xl">&#9734;</span>
                        </div>
                    </div>
                </div>

                <md-outlined-text-field
                    type="textarea"
                    label="Write Review"
                    placeholder="Share your Experience"
                    rows="3"
                    class="w-150 h-40">
                </md-outlined-text-field>

                <div class="w-150 flex justify-end">
                    <md-filled-button class="w-24 h-12" @click="toggleWriteReview">Post</md-filled-button>
                </div>
            </div>
        </div>

    </div>
</template>