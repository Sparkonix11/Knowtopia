<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  // Allow passing content through slots for flexibility
});
</script>

<template>
  <div class="w-[80%] h-fit px-12 py-18 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6 justify-center">
    <div class="text-center">
      <span class="text-3xl">{{ title }}</span>
    </div>
    
    <!-- Content slot for flexible content rendering -->
    <slot></slot>
  </div>
</template>