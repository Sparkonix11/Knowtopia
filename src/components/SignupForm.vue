<script setup>
import { useSignup } from "../handlers/useSignup";

const {
  selected,
  errorMessage,
  firstName,
  lastName,
  email,
  countryCode,
  phoneNumber,
  password,
  confirmPassword,
  errors,
  isSubmitting,
  is_instructor,
  updateFirstName,
  updateLastName,
  updateEmail,
  updateCountryCode,
  updatePhoneNumber,
  updatePassword,
  updateConfirmPassword,
  signup,
  handleInput
} = useSignup();
</script>

<template>
    <div class="flex flex-col gap-8 w-md ml-[12%]">
        <!-- User type selector -->
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

        <!-- Global error message -->
        <div v-if="errorMessage" class="text-red-500 text-sm font-medium">{{ errorMessage }}</div>

        <!-- Name fields -->
        <div class="flex gap-5 w-full">
            <div class="flex flex-col gap-1 w-full">
                <md-outlined-text-field 
                    label="First Name" 
                    placeholder="Enter First Name"
                    @input="updateFirstName"
                    :value="firstName"
                    :error="!!errors.firstName"
                    class="w-full"
                ></md-outlined-text-field>
                <div v-if="errors.firstName" class="text-red-500 text-xs ml-1">{{ errors.firstName }}</div>
            </div>
            <div class="flex flex-col gap-1 w-full">
                <md-outlined-text-field 
                    label="Last Name" 
                    placeholder="Enter Last Name"
                    @input="updateLastName"
                    :value="lastName"
                    :error="!!errors.lastName"
                    class="w-full"
                ></md-outlined-text-field>
                <div v-if="errors.lastName" class="text-red-500 text-xs ml-1">{{ errors.lastName }}</div>
            </div>
        </div>

        <!-- Email field -->
        <div class="flex flex-col gap-1">
            <md-outlined-text-field 
                label="Email Address" 
                placeholder="Enter Email address" 
                type="email"
                @input="updateEmail"
                :value="email"
                :error="!!errors.email"
            ></md-outlined-text-field>
            <div v-if="errors.email" class="text-red-500 text-xs ml-1">{{ errors.email }}</div>
        </div>

        <!-- Phone fields -->
        <div class="flex gap-5 w-full">
            <div class="flex flex-col gap-1">
                <md-outlined-text-field 
                    label="Code" 
                    :value="countryCode" 
                    @input="updateCountryCode"
                    :error="!!errors.countryCode"
                    class="w-26"
                ></md-outlined-text-field>
                <div v-if="errors.countryCode" class="text-red-500 text-xs ml-1">{{ errors.countryCode }}</div>
            </div>
            <div class="flex flex-col gap-1 w-full">
                <md-outlined-text-field 
                    label="Phone Number" 
                    placeholder="Enter Phone Number" 
                    type="tel" 
                    class="w-full"
                    @input="updatePhoneNumber"
                    :value="phoneNumber"
                    :error="!!errors.phoneNumber"
                ></md-outlined-text-field>
                <div v-if="errors.phoneNumber" class="text-red-500 text-xs ml-1">{{ errors.phoneNumber }}</div>
            </div>
        </div>

        <!-- Password fields -->
        <div class="flex gap-5 w-full">
            <div class="flex flex-col gap-1 w-full">
                <md-outlined-text-field 
                    label="Create Password" 
                    placeholder="Enter Password" 
                    type="password"
                    @input="updatePassword"
                    :value="password"
                    :error="!!errors.password"
                ></md-outlined-text-field>
                <div v-if="errors.password" class="text-red-500 text-xs ml-1">{{ errors.password }}</div>
            </div>
            <div class="flex flex-col gap-1 w-full">
                <md-outlined-text-field 
                    label="Confirm Password" 
                    placeholder="Enter Password" 
                    type="password"
                    @input="updateConfirmPassword"
                    :value="confirmPassword"
                    :error="!!errors.confirmPassword"
                ></md-outlined-text-field>
                <div v-if="errors.confirmPassword" class="text-red-500 text-xs ml-1">{{ errors.confirmPassword }}</div>
            </div>
        </div>

        <!-- Signup button with loading state -->
        <md-filled-button 
            class="h-14" 
            @click="signup"
            :disabled="isSubmitting"
        >
            <span v-if="isSubmitting">Creating Account...</span>
            <span v-else>Create Account</span>
        </md-filled-button>
        
        <!-- Login link -->
        <div class="text-center text-sm">
            Already have an account? 
            <router-link to="/login" class="text-(--md-sys-color-primary) hover:underline">
                Log in
            </router-link>
        </div>
    </div>
</template>