<script setup>
import SignupForm from '@/components/SignupForm.vue'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
    <Navbar/>
    <div class="h-[calc(100vh-5rem)] flex flex-col justify-center ">
        <SignupForm class="ml-30 "/>
    </div>
    
</template>