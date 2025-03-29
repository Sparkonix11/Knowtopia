<script setup>
import SignupForm from '@/components/SignupForm.vue'
import Navbar from '@/components/Navbar.vue'
import { DotLottieVue } from '@lottiefiles/dotlottie-vue'
</script>

<template>
    <Navbar/>
    <div class="h-[calc(100vh-5rem)] flex items-center justify-around ">
        <div class="flex flex-col items-start justify-center gap-10">
            <div class="text-center mx-auto">
                <span class="text-3xl font-bold text-gray-900 text-center block">
                Join 
                <span style="font-family: 'Lobster';" class=" text-blue-900 text-4xl drop-shadow-md">Knowtopia</span>
                </span>
                <span style="font-family: 'Poppins';" class="text-lg text-gray-700 italic tracking-wide block mt-2">
                    Where Curiosity Meets Knowledge!
                </span>
            </div>
            <SignupForm class="w-full"/>
        </div>
        <DotLottieVue style="height: 600px; width: 600px" autoplay loop src="https://lottie.host/108cea66-d88b-42eb-b982-0d7206e86a28/Ml68PIULpk.lottie" class="mr-30"/>

    </div>
    
</template>