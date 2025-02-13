<script setup>
</script>

<template>
    <div class="w-90 h-[calc(100vh-5rem)] bg-(--md-sys-color-surface-container-low) px-3 left-0">
        <div class="h-14 w-full flex items-center px-5">
            <span class="text-(length:--md-sys-typescale-title-medium-font)">Student Portal</span>
        </div>
        <div class="h-14 rounded-[100px] flex items-center gap-2 px-4 hover:bg-(--md-sys-color-on-surface2)">
            <md-icon>dashboard</md-icon>
            <span>Dashboard</span>
        </div>
        <div class="h-14 rounded-[100px] flex items-center gap-2 px-4 bg-(--md-sys-color-secondary-container)">
            <md-icon>book</md-icon>
            <span>My Courses</span>
        </div>
        <div class="h-14 rounded-[100px] flex items-center gap-2 px-4 hover:bg-(--md-sys-color-on-surface2)">
            <md-icon>menu_book</md-icon>
            <span>Study Material</span>
        </div>
        <div class="h-14 rounded-[100px] flex items-center gap-2 px-4 hover:bg-(--md-sys-color-on-surface2)">
            <md-icon>two_pager</md-icon>
            <span>Assignments</span>
        </div>
        <md-divider></md-divider>
        <div class="h-14 w-full flex items-center px-5 ">
            <span class="text-(length:--md-sys-typescale-title-medium-font)">Saved</span>
        </div>
        <div class="h-14 rounded-[100px] flex items-center gap-2 px-4 hover:bg-(--md-sys-color-on-surface2)">
            <md-icon>book_2</md-icon>
            <span>Notes</span>
        </div>
    </div>
   
</template>