<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import Sidebar from '@/components/Sidebar.vue';
import avatar from '@/assets/avatar.png';
</script>

<template>
    <NavbarMain />
    <div class="flex">
        <Sidebar />
        <div class="flex-1 flex flex-col items-center my-10 gap-6">
            <div class="w-[80%] h-fit px-12 py-18 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6 justify-center items-center">

                <div class="flex gap-2">
                    <img :src="avatar" alt="" class="w-30 h-30 rounded-full border border-(--md-sys-color-outline-variant)">

                    <div class="flex flex-col items-center justify-center gap-2">
                        <span class="text-2xl">Change Profile Picture</span>
                        <div class="flex gap-2">
                            <md-filled-button class="w-35 h-11">Change</md-filled-button>
                            <md-outlined-button class="w-35 h-11">Remove</md-outlined-button>
                        </div>
                    </div>

                </div>
            </div>
            <div class="w-[80%] h-fit px-12 py-14 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6 justify-center items-center">
                <span class="text-3xl my-8">Personal Information</span>

                <div class="flex flex-col w-full px-5 gap-10">

                    <div class="flex justify-evenly w-full">
                        <md-outlined-text-field label="First Name" placeholder="Enter First Name" class="w-150" />
                        <md-outlined-text-field label="Last Name" placeholder="Enter Last Name" class="w-150" />
                    </div>

                    <div class="flex justify-evenly w-full">
                        <md-outlined-text-field label="Date of Birth" placeholder="01/01/2000" class="w-150" />
                        <div class="w-150 px-5">
                            <div class="flex flex-col gap-2">
                                <span class="text-lg px-2">Gender</span>
                                <div class="flex justify-between items-center">
                                    <div class="flex gap-4">
                                        <md-radio id="male" name="Gender" value="male"></md-radio>
                                        <label for="male">Male</label>
                                    </div>

                                    <div class="flex gap-4">
                                        <md-radio id="female" name="Gender" value="female"></md-radio>
                                        <label for="female">Female</label>
                                    </div>

                                    <div class="flex gap-4">
                                        <md-radio id="others" name="Gender" value="others"></md-radio>
                                        <label for="others">Others</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="flex justify-evenly w-full">
                        <div class="flex w-150 gap-2">
                            <md-outlined-text-field label="Code" value="+91" class="w-26"></md-outlined-text-field>
                            <md-outlined-text-field label="Phone Number" placeholder="Enter Phone Number" type="tel" class="w-full"></md-outlined-text-field>
                        </div>
                        <md-outlined-text-field label="About" placeholder="Enter Bio Details" class="w-150" />
                    </div>

                </div>
            </div>

            <div class="w-[80%] h-fit px-12 py-12 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6 justify-center items-center">
                <span class="text-3xl my-2">Password</span>

                <div class="flex justify-evenly w-full">
                    <md-outlined-text-field label="Current Password" placeholder="Enter Current Password" type="password" class="w-150"></md-outlined-text-field>
                    <md-outlined-text-field label="New Password" placeholder="Enter New Password" type="password" class="w-150"></md-outlined-text-field>
                </div>
            </div>

            <div class="flex justify-end w-[80%] gap-4">
                <md-outlined-button class="w-35 h-11">Cancel</md-outlined-button>
                <md-filled-button class="w-35 h-11">Save</md-filled-button>
            </div>

        </div>
    </div>

</template>