<script setup>
import LoginForm from '@/components/LoginForm.vue'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
    <Navbar/>
    <div class="h-[calc(100vh-5rem)] flex flex-col justify-center ">
        <LoginForm class="ml-30 "/>
    </div>
    
</template>