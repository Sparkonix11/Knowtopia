<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();
import logo from '@/assets/logo.png';
</script>

<template>
    <div class="navbar flex w-full items-center justify-around h-20 bg-(--md-sys-color-surface-container)">
        <div class="flex-1 flex justify-center items-center gap-2">
            <img :src="logo" alt="" class="w-20 h-20 rounded-full ">
            <span style="font-family: 'Lobster';" class="text-2xl text-(--md-sys-color-primary)">Knowtopia</span>
        </div>
        <div class="flex-1"></div>
        <!-- <div class="relative flex items-center">
            <input type="text" placeholder="Search Bar" class="w-147 h-14 rounded-[28px] border-1 p-2 px-8">
            <md-icon-button class="absolute right-4">
                <md-icon>search</md-icon>
            </md-icon-button> 
        </div> -->
        <div class="flex flex-1 items-center justify-center gap-3">
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
