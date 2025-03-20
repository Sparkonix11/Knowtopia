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
  is_instructor,
  updateFirstName,
  updateLastName,
  updateEmail,
  updateCountryCode,
  updatePhoneNumber,
  updatePassword,
  updateConfirmPassword,
  signup
} = useSignup();
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

        <div v-if="errorMessage" class="text-red-500">{{ errorMessage }}</div>

        <div class="flex gap-5 w-full">
            <md-outlined-text-field 
                label="First Name" 
                placeholder="Enter First Name"
                @input="updateFirstName"
                :value="firstName"
            ></md-outlined-text-field>
            <md-outlined-text-field 
                label="Last Name" 
                placeholder="Enter Last Name"
                @input="updateLastName"
                :value="lastName"
            ></md-outlined-text-field>
        </div>

        <md-outlined-text-field 
            label="Email Address" 
            placeholder="Enter Email address" 
            type="email"
            @input="updateEmail"
            :value="email"
        ></md-outlined-text-field>

        <div class="flex gap-5 w-full">
            <md-outlined-text-field 
                label="Code" 
                :value="countryCode" 
                @input="updateCountryCode"
                class="w-26"
            ></md-outlined-text-field>
            <md-outlined-text-field 
                label="Phone Number" 
                placeholder="Enter Phone Number" 
                type="tel" 
                class="w-full"
                @input="updatePhoneNumber"
                :value="phoneNumber"
            ></md-outlined-text-field>
        </div>

        <div class="flex gap-5 w-full">
            <md-outlined-text-field 
                label="Create Password" 
                placeholder="Enter Password" 
                type="password"
                @input="updatePassword"
                :value="password"
            ></md-outlined-text-field>
            <md-outlined-text-field 
                label="Confirm Password" 
                placeholder="Enter Password" 
                type="password"
                @input="updateConfirmPassword"
                :value="confirmPassword"
            ></md-outlined-text-field>
        </div>

        <md-filled-button class="h-14" @click="signup">Create Account</md-filled-button>
    </div>
</template>