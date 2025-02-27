<script setup>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useStore();


const selected = ref("student");
const errorMessage = ref("");
const email = ref("");
const password = ref("");

const updateEmail = (event) => {
    email.value = event.target.value;
};
const updatePassword = (event) => {
    password.value = event.target.value;
};

const user = computed(() => store.getters["user/currentUser"]);


const login = async () => {
    errorMessage.value = "";
    if (!email.value.trim() || !password.value.trim()) {
        errorMessage.value = "Please enter both email and password.";
        return;
    }
    const formData = new FormData();
    formData.append('email', email.value);
    formData.append('password', password.value);

    const response = await store.dispatch("user/login", formData);

    if (response.status === 200) {
        if (!user.value?.is_instructor) {
            router.push({ name: "StudentDashboard" });
        } else {
            router.push({ name: "InstructorDashboard" });
        }
    } else {
        errorMessage.value = response.message || "Login failed. Please try again.";
    }
};
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

        <md-outlined-text-field
            @input="updateEmail"
            label="Email Address"
            placeholder="Enter Email address"
            type="email"
            :value="email"
        ></md-outlined-text-field>

        <md-outlined-text-field
            @input="updatePassword"
            v-model="password"
            label="Password"
            placeholder="Enter Password"
            type="password"
            :value="password"
        ></md-outlined-text-field>

        <md-filled-button class="w-full h-14" @click="login">Login</md-filled-button>
    </div>
</template>