<script setup>
import { ref } from "vue";
const selected = ref("student");
</script>
<template>
    <div class="flex flex-col gap-8 w-md ml-[12%]">
        <div class="flex rounded-full w-60">
            <button
            @click="selected = 'student'"
            :class="[
                'flex-1 py-2 rounded-full rounded-r-none transition border border-r-0 border-(--md-sys-color-outline) flex items-center justify-center gap-1 ',
                selected === 'student' ? 'bg-(--md-sys-color-secondary-container)' : 'bg-transparent',
            ]"
            >
            <md-icon v-if="selected === 'student'">check</md-icon>
            Student
            </button>
            <button
            @click="selected = 'instructor'"
            :class="[
                'flex-1 py-2 rounded-full rounded-l-none transition border border-(--md-sys-color-outline) flex items-center justify-center gap-1 ',
                selected === 'instructor' ? 'bg-(--md-sys-color-secondary-container)' : 'bg-transparent',
            ]"
            >
            <md-icon v-if="selected === 'instructor'">check</md-icon>
            Instructor
            </button>
        </div>


        <div class="flex gap-5 w-full">
            <md-outlined-text-field label="First Name" placeholder="Enter First Name"></md-outlined-text-field>
            <md-outlined-text-field label="Last Name" placeholder="Enter Last Name"></md-outlined-text-field>
        </div>

        <md-outlined-text-field label="Email Address" placeholder="Enter Email address" type="email"></md-outlined-text-field>

        <div class="flex gap-5 w-full">
            <md-outlined-text-field label="Code" value="+91" class="w-26"></md-outlined-text-field>
            <!-- <md-outlined-select class="min-w-26 ">
                <md-select-option selected value="+91">
                    <div slot="headline">+91</div>
                </md-select-option>
                <md-select-option value="+1">
                    <div slot="headline">+1</div>
                </md-select-option>
            </md-outlined-select> -->
            <md-outlined-text-field label="Phone Number" placeholder="Enter Phone Number" type="tel" class="w-full"></md-outlined-text-field>
        </div>

        <div class="flex gap-5 w-full">
            <md-outlined-text-field label="Create Password" placeholder="Enter Password" type="password"></md-outlined-text-field>
            <md-outlined-text-field label="Confirm Password" placeholder="Enter Password" type="password"></md-outlined-text-field>
        </div>

        <md-filled-button class=" h-14">Create Account</md-filled-button>
    </div>
</template>

