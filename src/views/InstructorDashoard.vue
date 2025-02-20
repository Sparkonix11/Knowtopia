<script setup>
import NavbarMain from '@/components/NavbarMain.vue';
import Sidebar from '@/components/Sidebar.vue';
import avatar from '@/assets/avatar.png';
import marksChart from '@/assets/instructor_marks_chart.png';
import doubtChart from '@/assets/instructor_doubts_chart.png';
</script>

<template>
<NavbarMain />
<div class="flex">
    <Sidebar />
    <div class="flex-1 flex flex-col items-center my-10 gap-6">
        <div class="w-[80%] h-fit px-12 py-18 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6">
            <div class="text-center">
                <span class="text-3xl">Reviews</span>
            </div>

            <div class="flex w-full justify-evenly">
                <div class="flex flex-col w-90 gap-4">
                    <div class="flex gap-4 justify-around mt-8">
                        <div class="flex items-center gap-2">
                            <img :src="avatar" alt="" class="w-28 h-28 rounded-full">
                            <div class="flex-col justify-center items-center text-center">
                                <span class=" text-xl">User Name</span>
                                <div class="flex items-center">
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9734;</span>
                                </div>

                            </div>

                        </div>
                    </div>

                    <div class=" text-justify text-base">
                        <span>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed rutrum ligula. Duis massa diam, mollis vel vehicula at, tempor et urna. Maecenas eget mi tortor. Maecenas a vehicula lorem.</span>
                    </div>
                </div>

                <div class="flex flex-col w-90 gap-4">
                    <div class="flex gap-4 justify-around mt-8">
                        <div class="flex items-center gap-2">
                            <img :src="avatar" alt="" class="w-28 h-28 rounded-full">
                            <div class="flex-col justify-center items-center text-center">
                                <span class=" text-xl">User Name 2</span>
                                <div class="flex items-center">
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9734;</span>
                                    <span class=" text-3xl">&#9734;</span>
                                </div>

                            </div>

                        </div>
                    </div>

                    <div class=" text-justify text-base">
                        <span>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed rutrum ligula. Duis massa diam, mollis vel vehicula at, tempor et urna. Maecenas eget mi tortor. Maecenas a vehicula lorem.</span>
                    </div>
                </div>

                <div class="flex flex-col w-90 gap-4">
                    <div class="flex gap-4 justify-around mt-8">
                        <div class="flex items-center gap-2">
                            <img :src="avatar" alt="" class="w-28 h-28 rounded-full">
                            <div class="flex-col justify-center items-center text-center">
                                <span class=" text-xl">User Name 3</span>
                                <div class="flex items-center">
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9733;</span>
                                    <span class=" text-3xl">&#9733;</span>
                                </div>

                            </div>

                        </div>
                    </div>

                    <div class=" text-justify text-base">
                        <span>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed rutrum ligula. Duis massa diam, mollis vel vehicula at, tempor et urna. Maecenas eget mi tortor. Maecenas a vehicula lorem.</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="w-[80%] h-fit px-12 py-18 bg-(--md-sys-color-surface) border border-(--md-sys-color-outline-variant) rounded-[12px] m-auto flex flex-col gap-6">
            <div class="text-center">
                <span class="text-3xl">Statistics</span>
            </div>

            <div class="flex justify-evenly">
                <img :src="marksChart" alt="" class="w-[40%]">
                <img :src="doubtChart" alt="" class="w-[40%]">

            </div>
        </div>

    </div>
</div>

</template>