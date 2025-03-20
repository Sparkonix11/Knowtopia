<script setup>
import { useLogin } from "../handlers/useLogin";

const {
  selected,
  errorMessage,
  email,
  password,
  updateEmail,
  updatePassword,
  login
} = useLogin();
</script>

<template>
    <div class="flex flex-col gap-8 w-md ml-[12%]">
        <!-- <div class="flex rounded-full w-60">
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
        </div> -->

        <div v-if="errorMessage" class="text-red-500">{{ errorMessage }}</div>

        <md-outlined-text-field
            @input="updateEmail"
            label="Email Address"
            placeholder="Enter Email address"
            type="email"
            :value="email"
        ></md-outlined-text-field>

        <md-outlined-text-field
            @input="updatePassword"
            label="Password"
            placeholder="Enter Password"
            type="password"
            :value="password"
        ></md-outlined-text-field>

        <md-filled-button class="w-full h-14" @click="login">Login</md-filled-button>
    </div>
</template>