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
  <NavbarMain class="fixed top-0 left-0 right-0 z-20" />
  <div class="flex pt-20">
    <Sidebar />
    <div class="flex-1 flex flex-col w-full px-6 ml-[20%]" :class="contentClass">
      <!-- Content slot for page-specific content -->
      <slot></slot>
    </div>
  </div>
</template>