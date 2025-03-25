<script setup>
import avatarPlaceholder from '@/assets/avatar.png';
import { useWriteReview } from '@/handlers/useWriteReview';
import { computed } from 'vue';

const props = defineProps({
    materialId: {
        type: String,
        required: true
    }
});

const emit = defineEmits(["toggleWriteReview"]);
const toggleWriteReview = () => {
    emit("toggleWriteReview");
};

// Use the handler to manage form state and logic
const {
    user,
    formState,
    errors,
    isSubmitting,
    submitError,
    hoverRating,
    success,
    setRating,
    setHoverRating,
    resetHoverRating,
    submitForm,
    updateField
} = useWriteReview(props.materialId, toggleWriteReview);
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
                    <img :src="user?.image ? `../../server${user.image}` : avatarPlaceholder" alt="User profile" class="w-28 h-28 rounded-full object-cover">
                    <div class="flex-col justify-center items-center text-center">
                        <span class="text-xl">{{ user ? `${user.fname} ${user.lname}` : 'User' }}</span>
                        <div class="flex items-center">
                            <span 
                                v-for="star in 5" 
                                :key="star" 
                                class="text-3xl cursor-pointer" 
                                :class="{
                                    'text-yellow-500': (hoverRating || formState.rating) >= star,
                                    'text-gray-300': (hoverRating || formState.rating) < star
                                }"
                                @click="setRating(star)"
                                @mouseenter="setHoverRating(star)"
                                @mouseleave="resetHoverRating"
                            >
                                &#9733;
                            </span>
                        </div>
                    </div>
                </div>

                <md-outlined-text-field
                    type="textarea"
                    label="Write Review"
                    placeholder="Share your Experience"
                    rows="3"
                    class="w-150 h-40"
                    v-model="formState.comment"
                    @input="updateField('comment', $event.target.value)">
                </md-outlined-text-field>
                
                <div v-if="errors.rating || errors.comment || submitError" class="w-150 text-red-500 text-sm">
                    {{ errors.rating || errors.comment || submitError }}
                </div>
                
                <div v-if="success" class="w-150 text-green-500 text-sm">
                    Review submitted successfully!
                </div>

                <div class="w-150 flex justify-end">
                    <md-filled-button 
                        class="w-24 h-12" 
                        @click="submitForm"
                        :disabled="isSubmitting"
                    >
                        <md-circular-progress v-if="isSubmitting" indeterminate class="mr-2"></md-circular-progress>
                        {{ isSubmitting ? 'Posting...' : 'Post' }}
                    </md-filled-button>
                </div>
            </div>
        </div>

    </div>
</template>