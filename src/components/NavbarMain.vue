<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const menuOpen = ref(false);

const toggleMenu = () => {
    menuOpen.value = !menuOpen.value;
};
</script>

<template>
    <div class="navbar flex w-full items-center justify-between px-30 h-20 bg-(--md-sys-color-surface-container)">
        <div></div>
        <div class="relative flex items-center">
            <input type="text" placeholder="Search Bar" class="w-147 h-14 rounded-[28px] border-1 p-2 px-8">
            <md-icon-button class="absolute right-4">
                <md-icon>search</md-icon>
            </md-icon-button> 
        </div>
        <div class="flex gap-3 items-center">
            <md-filled-icon-button>
                <md-icon>chat</md-icon>
            </md-filled-icon-button>
            <md-filled-icon-button>
                <md-icon>notifications</md-icon>
            </md-filled-icon-button>
            <span class="relative">
                <md-filled-button @click="toggleMenu" id="user-menu"><img src="../assets/avatar.png" alt="user" class="h-12 w-12 rounded-full border-2 border-(--md-sys-color-primary)"></md-filled-button>
                <md-menu id="usage-menu" :open="menuOpen" anchor="user-menu">
                    <md-menu-item class="w-50">
                        <div class="flex justify-baseline gap-4 px-2">
                            <md-icon>settings</md-icon>
                            <div>Profile Settings</div>
                        </div>
                    </md-menu-item>
                    <md-menu-item>
                        <div class="flex justify-baseline gap-4 px-2">
                            <md-icon>share</md-icon>
                            <div>Share Profile</div>
                        </div>
                    </md-menu-item>
                    <md-divider></md-divider>
                    <md-menu-item>
                        <div class=" text-center">Logout</div>
                    </md-menu-item>
                </md-menu>
            </span>
        </div>
    </div>
</template>