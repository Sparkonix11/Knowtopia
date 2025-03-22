<script setup>
import { ref, computed, reactive } from 'vue';
import { useStore } from 'vuex';
import BaseLayout from '@/components/BaseLayout.vue';
import avatarPlaceholder from '@/assets/avatar.png';

const store = useStore();
const user = computed(() => store.getters["user/currentUser"]).value;
const pfp = '../../server'+user.image;

// Feedback state
const feedback = reactive({
    show: false,
    message: '',
    type: 'success' // 'success' or 'error'
});

// Function to show feedback message
const showFeedback = (message, type = 'success') => {
    feedback.message = message;
    feedback.type = type;
    feedback.show = true;
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        feedback.show = false;
    }, 3000);
};

const profileImage = ref(pfp || avatarPlaceholder);
const firstName = ref(user.fname || '');
const lastName = ref(user.lname || '');
const dateOfBirth = ref(user.dob || '');
const gender = ref(user.gender || '');
const phoneCode = ref(user.phone ? user.phone.slice(0, 3) : '+91');
const phoneNumber = ref(user.phone ? user.phone.slice(3) : '');
const about = ref(user.about || '');
const currentPassword = ref('');
const newPassword = ref('');

const updateFirstName = (event) => { firstName.value = event.target.value; };
const updateLastName = (event) => { lastName.value = event.target.value; };
const updateDateOfBirth = (event) => { dateOfBirth.value = event.target.value; };
const updateGender = (event) => { gender.value = event.target.value; };
const updatePhoneCode = (event) => { phoneCode.value = event.target.value; };
const updatePhoneNumber = (event) => { phoneNumber.value = event.target.value; };
const updateAbout = (event) => { about.value = event.target.value; };
const updateCurrentPassword = (event) => { currentPassword.value = event.target.value; };
const updateNewPassword = (event) => { newPassword.value = event.target.value; };

const fileInput = ref(null);

const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        profileImage.value = URL.createObjectURL(file);
    }
};



const triggerFileInput = () => {
    fileInput.value.click();
};

const saveProfile = async () => {
    const formData = new FormData();
    formData.append('fname', firstName.value);
    formData.append('lname', lastName.value);
    formData.append('dob', dateOfBirth.value);
    formData.append('gender', gender.value);
    formData.append('phone', phoneCode.value + phoneNumber.value);
    formData.append('about', about.value);
    formData.append('current_password', currentPassword.value);
    formData.append('new_password', newPassword.value);

    if (fileInput.value.files[0]) {
        formData.append('image', fileInput.value.files[0]);
    }

    try {
        const response = await store.dispatch("user/updateUserProfile", formData);
        
        if (response.status === 200) {
            showFeedback("Profile updated successfully", "success");
            // Clear password fields after successful update
            currentPassword.value = '';
            newPassword.value = '';
        } else {
            showFeedback(response.message || "Update failed. Please try again.", "error");
        }
    } catch (error) {
        showFeedback(error.message || "Update failed. Please try again.", "error");
    }
};
</script>

<template>
    <BaseLayout>
            <!-- Feedback notification -->
            <div v-if="feedback.show" 
                 class="fixed top-5 right-5 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 max-w-md"
                 :class="feedback.type === 'success' ? 'bg-(--md-sys-color-primary-container) text-(--md-sys-color-on-primary-container)' : 'bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container)'">
                <div class="flex items-center gap-2">
                    <md-icon>{{ feedback.type === 'success' ? 'check_circle' : 'error' }}</md-icon>
                    <span>{{ feedback.message }}</span>
                </div>
            </div>
            <div class="w-[80%] h-fit px-12 py-18 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6 justify-center items-center">
                <div class="flex gap-2">
                    <img :src="profileImage" alt="Profile Picture" class="w-30 h-30 rounded-full border border-(--md-sys-color-outline-variant)">
                    <div class="flex flex-col items-center justify-center gap-2">
                        <span class="text-2xl">Change Profile Picture</span>
                        <div class="flex gap-2">
                            <input type="file" ref="fileInput" class="hidden" @change="handleFileChange">
                            <md-filled-button class="w-35 h-11" @click="triggerFileInput">Change</md-filled-button>
                            <md-outlined-button class="w-35 h-11" @click="profileImage = avatarPlaceholder">Remove</md-outlined-button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="w-[80%] h-fit px-12 py-14 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6 justify-center items-center">
                <span class="text-3xl my-8">Personal Information</span>
                <div class="flex flex-col w-full px-5 gap-10">
                    <div class="flex justify-evenly w-full">
                        <md-outlined-text-field label="First Name" placeholder="Enter First Name" @input="updateFirstName" :value="firstName" class="w-150" />
                        <md-outlined-text-field label="Last Name" placeholder="Enter Last Name" @input="updateLastName" :value="lastName" class="w-150" />
                    </div>

                    <div class="flex justify-evenly w-full">
                        <md-outlined-text-field label="Date of Birth" placeholder="01-01-2000" @input="updateDateOfBirth" :value="dateOfBirth" class="w-150" />
                        <div class="w-150 px-5">
                            <div class="flex flex-col gap-2">
                                <span class="text-lg px-2">Gender</span>
                                <div class="flex justify-between items-center">
                                    <div class="flex gap-4">
                                        <md-radio id="male" name="Gender" value="male" @change="updateGender" :checked="gender === 'male'"></md-radio>
                                        <label for="male">Male</label>
                                    </div>
                                    <div class="flex gap-4">
                                        <md-radio id="female" name="Gender" value="female" @change="updateGender" :checked="gender === 'female'"></md-radio>
                                        <label for="female">Female</label>
                                    </div>
                                    <div class="flex gap-4">
                                        <md-radio id="others" name="Gender" value="others" @change="updateGender" :checked="gender === 'others'"></md-radio>
                                        <label for="others">Others</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="flex justify-evenly w-full">
                        <div class="flex w-150 gap-2">
                            <md-outlined-text-field label="Code" @input="updatePhoneCode" :value="phoneCode" class="w-26"></md-outlined-text-field>
                            <md-outlined-text-field label="Phone Number" type="tel" @input="updatePhoneNumber" :value="phoneNumber" class="w-full"></md-outlined-text-field>
                        </div>
                        <md-outlined-text-field label="About" @input="updateAbout" :value="about" class="w-150" />
                    </div>
                </div>
            </div>

            <div class="w-[80%] h-fit px-12 py-12 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6 justify-center items-center">
                <span class="text-3xl my-2">Password</span>
                <div class="flex justify-evenly w-full">
                    <md-outlined-text-field label="Current Password" type="password" @input="updateCurrentPassword" :value="currentPassword" class="w-150"></md-outlined-text-field>
                    <md-outlined-text-field label="New Password" type="password" @input="updateNewPassword" :value="newPassword" class="w-150"></md-outlined-text-field>
                </div>
            </div>

            <div class="flex justify-end w-[80%] gap-4">
                <md-outlined-button class="w-35 h-11" @click="() => {
                    // Reset form to original user data
                    profileImage.value = pfp || avatarPlaceholder;
                    firstName.value = user.fname || '';
                    lastName.value = user.lname || '';
                    dateOfBirth.value = user.dob || '';
                    gender.value = user.gender || '';
                    phoneCode.value = user.phone ? user.phone.slice(0, 3) : '+91';
                    phoneNumber.value = user.phone ? user.phone.slice(3) : '';
                    about.value = user.about || '';
                    currentPassword.value = '';
                    newPassword.value = '';
                    showFeedback('Form reset to original values');
                }">Cancel</md-outlined-button>
                <md-filled-button class="w-35 h-11" @click="saveProfile">Save</md-filled-button>
            </div>
    </BaseLayout>
</template>