<script setup>
import {RouterLink, RouterView} from 'vue-router'
import { onMounted } from 'vue';

onMounted(() => {
  document.body.classList.add('light');
});
</script>

<template>
  <RouterView />
</template>