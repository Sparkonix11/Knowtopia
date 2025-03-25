<script setup>
import { defineProps } from 'vue';
import avatar from '@/assets/avatar.png';

const props = defineProps({
  username: {
    type: String,
    default: 'User Name'
  },
  rating: {
    type: Number,
    default: 4
  },
  review: {
    type: String,
    default: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed rutrum ligula. Duis massa diam, mollis vel vehicula at, tempor et urna. Maecenas eget mi tortor.'
  },
  userImage: {
    type: String,
    default: null
  }
});

// Use the provided image or fallback to the default avatar
const userAvatar = props.userImage ? `../../server${props.userImage}` : avatar;
</script>

<template>
  <div class="flex flex-col w-90 gap-4">
    <div class="flex gap-4 justify-around mt-8">
      <div class="flex items-center gap-2">
        <img :src="userAvatar" alt="User profile" class="w-28 h-28 rounded-full object-cover">
        <div class="flex-col justify-center items-center text-center">
          <span class="text-xl">{{ username }}</span>
          <div class="flex items-center">
            <span v-for="i in 5" :key="i" class="text-3xl" :class="{ 'text-yellow-400': i <= rating }">
              {{ i <= rating ? '★' : '☆' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="text-justify text-base">
      <span>{{ review }}</span>
    </div>
  </div>
</template>