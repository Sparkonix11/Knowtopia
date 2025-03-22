<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import Sidebar from '@/components/Sidebar.vue';

// Define props to allow customization of the layout
const props = defineProps({
  // Optional class for the content container
  contentClass: {
    type: String,
    default: 'my-10 gap-6'
  }
});
</script>

<template>
  <NavbarMain />
  <div class="flex">
    <Sidebar />
    <div class="flex-1 flex flex-col items-center" :class="contentClass">
      <!-- Content slot for page-specific content -->
      <slot></slot>
    </div>
  </div>
</template>