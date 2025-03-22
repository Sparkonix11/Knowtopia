<script setup>
import { useLogin } from "../handlers/useLogin";

const {
  selected,
  errorMessage,
  email,
  password,
  errors,
  isSubmitting,
  updateEmail,
  updatePassword,
  login,
  handleInput
} = useLogin();
</script>

<template>
    <div class="flex flex-col gap-8 w-md ml-[12%]">
        <!-- Global error message -->
        <div v-if="errorMessage" class="text-red-500 text-sm font-medium">{{ errorMessage }}</div>

        <!-- Email field -->
        <div class="flex flex-col gap-1">
            <md-outlined-text-field
                @input="updateEmail"
                label="Email Address"
                placeholder="Enter Email address"
                type="email"
                :value="email"
                :error="!!errors.email"
            ></md-outlined-text-field>
            <div v-if="errors.email" class="text-red-500 text-xs ml-1">{{ errors.email }}</div>
        </div>

        <!-- Password field -->
        <div class="flex flex-col gap-1">
            <md-outlined-text-field
                @input="updatePassword"
                label="Password"
                placeholder="Enter Password"
                type="password"
                :value="password"
                :error="!!errors.password"
            ></md-outlined-text-field>
            <div v-if="errors.password" class="text-red-500 text-xs ml-1">{{ errors.password }}</div>
        </div>

        <!-- Login button with loading state -->
        <md-filled-button 
            class="w-full h-14" 
            @click="login"
            :disabled="isSubmitting"
        >
            <span v-if="isSubmitting">Logging in...</span>
            <span v-else>Login</span>
        </md-filled-button>

        <!-- Signup link -->
        <div class="text-center text-sm">
            Don't have an account? 
            <router-link to="/signup" class="text-(--md-sys-color-primary) hover:underline">
                Sign up
            </router-link>
        </div>
    </div>
</template>