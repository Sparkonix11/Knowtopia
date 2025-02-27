<script setup>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useStore();

const selected = ref("student");
const errorMessage = ref("");

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const countryCode = ref("+91");
const phoneNumber = ref("");
const password = ref("");
const confirmPassword = ref("");

const is_instructor = computed(() => selected.value === "instructor");

const fullPhoneNumber = computed(() => countryCode.value + phoneNumber.value);

const user = computed(() => store.getters["user/currentUser"]);

// Update handlers
const updateFirstName = (event) => {
    firstName.value = event.target.value;
};
const updateLastName = (event) => {
    lastName.value = event.target.value;
};
const updateEmail = (event) => {
    email.value = event.target.value;
};
const updateCountryCode = (event) => {
    countryCode.value = event.target.value;
};
const updatePhoneNumber = (event) => {
    phoneNumber.value = event.target.value;
};
const updatePassword = (event) => {
    password.value = event.target.value;
};
const updateConfirmPassword = (event) => {
    confirmPassword.value = event.target.value;
};

const signup = async () => {
    errorMessage.value = "";
    
    // Validation
    if (!firstName.value.trim() || !lastName.value.trim()) {
        errorMessage.value = "Please enter both first and last name.";
        return;
    }
    
    if (!email.value.trim()) {
        errorMessage.value = "Please enter your email address.";
        return;
    }
    
    if (!phoneNumber.value.trim()) {
        errorMessage.value = "Please enter your phone number.";
        return;
    }
    
    if (!password.value.trim() || !confirmPassword.value.trim()) {
        errorMessage.value = "Please enter both password fields.";
        return;
    }
    
    if (password.value !== confirmPassword.value) {
        errorMessage.value = "Passwords do not match.";
        return;
    }
    
    // Create FormData for submission
    const formData = new FormData();
    formData.append('is_instructor', is_instructor.value);
    formData.append('fname', firstName.value);
    formData.append('lname', lastName.value);
    formData.append('email', email.value);
    formData.append('phone', fullPhoneNumber.value);
    formData.append('password', password.value);
    formData.append('password_confirm', confirmPassword.value);

    
    try {
        const response = await store.dispatch("user/signup", formData);
        
        if (response.status === 201) {
            if (!user.value?.is_instructor) {
            router.push({ name: "StudentDashboard" });
            } else {
                router.push({ name: "InstructorDashboard" });
            }
        } else {
            errorMessage.value = response.message || "Registration failed. Please try again.";
        }
    } catch (error) {
        errorMessage.value = error.message || "Registration failed. Please try again.";
    }
};
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