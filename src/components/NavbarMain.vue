<script setup>
import { ref, computed } from 'vue';
import logo from '@/assets/logo.png';
import { useStore } from 'vuex';
import ChatComponent from './ChatComponent.vue';

const menuOpen = ref(false);
const chatOpen = ref(false);
const notifOpen = ref(false);

const store = useStore();
const user = computed(() => store.getters["user/currentUser"]);

// Use the provided image or fallback to a default avatar
const avatar = user.value.image ? `../../server${user.value.image}` : '';

// Get current material ID if available (from route or parent component)
const props = defineProps({
    currentMaterialId: {
        type: [Number, String],
        default: null
    }
});

const toggleMenu = () => {
    menuOpen.value = !menuOpen.value;
    if (chatOpen.value) {
        chatOpen.value = false;
    }
    if (notifOpen.value) {
        notifOpen.value = false;
    }
};
const toggleChat = () => {
    chatOpen.value = !chatOpen.value;
    if (menuOpen.value) {
        menuOpen.value = false;
    }
    if (notifOpen.value) {
        notifOpen.value = false;
    }
};
const toggleNotif = () => {
    notifOpen.value = !notifOpen.value;
    if (menuOpen.value) {
        menuOpen.value = false;
    }
    if (chatOpen.value) {
        chatOpen.value = false;
    }
};
</script>

<template>
    <div class="navbar flex w-full items-center justify-between px-30 h-20 bg-(--md-sys-color-surface-container) shadow-md">
        <div class="flex-1 flex justify-start items-center pl-20 ">
            <router-link :to="{ name: user?.is_instructor ? 'InstructorDashboard' : 'StudentDashboard' }">
                <img :src="logo" alt="" class="w-20 h-20 rounded-full cursor-pointer">
            </router-link>
        </div>

        <div class="flex-1 flex items-center justify-center">
            <div class="relative flex items-center justify-center">
                <input type="text" placeholder="Search Bar" class="w-147 h-14 rounded-[28px] border-1 p-2 px-8">
                <md-icon-button class="absolute right-4">
                    <md-icon>search</md-icon>
                </md-icon-button> 
            </div>
        </div>

        <div class="flex flex-1 gap-3 items-center justify-center">

            <span class="relative">
                <md-filled-icon-button @click="toggleChat" id="user-menu">
                    <md-icon>chat</md-icon>
                </md-filled-icon-button>
                <md-menu id="chat-ai" :open="chatOpen" anchor="user-menu">
                    <div class="w-full sm:w-80 md:w-96 pt-2 pb-2">
                        <ChatComponent :current-material-id="props.currentMaterialId" />
                    </div>
                </md-menu>
            </span>

            <span class="relative">
                <md-filled-icon-button @click="toggleNotif" id="user-menu">
                    <md-icon>notifications</md-icon>
                </md-filled-icon-button>
                <md-menu id="chat-ai" :open="notifOpen" anchor="user-menu">
                    <div class="w-100 py-8 px-6 flex  gap-8 items-center justify-center">
                        <div class="flex items-center justify-center text-center gap-2">
                            <span>No New Notification</span>
                        </div>
                    </div>
                </md-menu>
            </span>

            <span class="relative">
                <md-filled-button @click="toggleMenu" id="user-menu"><img :src="avatar" alt="user" class="h-12 w-12 rounded-full border-2 border-(--md-sys-color-primary)"></md-filled-button>
                <md-menu id="usage-menu" :open="menuOpen" anchor="user-menu">
                    <router-link :to="{ name: 'Profile'}">
                    <md-menu-item class="w-50">
                        <div class="flex justify-baseline gap-4 px-2">
                            <md-icon>settings</md-icon>
                            <div>Profile Settings</div>
                        </div>
                    </md-menu-item>
                    </router-link>

                    <md-menu-item>
                        <div class="flex justify-baseline gap-4 px-2">
                            <md-icon>share</md-icon>
                            <div>Share Profile</div>
                        </div>
                    </md-menu-item>
                    <md-divider></md-divider>

                    <router-link :to="{ name: 'Login' }">
                        <md-menu-item>
                            <div class=" text-center">Logout</div>
                        </md-menu-item>
                    </router-link>
                </md-menu>
            </span>
        </div>
        
    </div>
</template>