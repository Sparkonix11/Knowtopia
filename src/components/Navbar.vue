<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();
</script>

<template>
    <div class="navbar flex w-full items-center justify-around h-20 bg-(--md-sys-color-surface-container)">
        <div></div>
        <div class="relative flex items-center">
            <input type="text" placeholder="Search Bar" class="w-147 h-14 rounded-[28px] border-1 p-2 px-8">
            <md-icon-button class="absolute right-4">
                <md-icon>search</md-icon>
            </md-icon-button> 
        </div>
        <div class="flex gap-3">
            <router-link :to="{ name: 'Login' }">
                <component 
                    :is="route.name === 'Login' ? 'md-outlined-button' : 'md-filled-button'"
                    class="w-24 h-12">
                    Login
                </component>
            </router-link>
            
            <router-link :to="{ name: 'Signup' }">
                <component 
                    :is="route.name === 'Signup' ? 'md-outlined-button' : 'md-filled-button'"
                    class="w-24 h-12">
                    Sign Up
                </component>
            </router-link>
        </div>
    </div>
</template>
