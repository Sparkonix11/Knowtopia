<script setup>
import CreateSubLectureView from './CreateSubLectureView.vue';
import CreateLecture from '../components/CreateLecture.vue';
import { ref, computed, onMounted } from 'vue';
import { useCreateLectures } from '../handlers/useCreateLectures';
import { useStore } from 'vuex';
import { deleteWeekAPI } from '../services/operations/weekAPI';
import { deleteMaterialAPI } from '../services/operations/materialAPI';

const store = useStore();

const { creatingCourse, creatingCourseWeeks, updateWeeks } = useCreateLectures();

const lectures = computed(() => creatingCourseWeeks.value);
const isLoading = ref(false);
const error = ref(null);

// Initialize the component
onMounted(async () => {
    isLoading.value = true;
    try {
        await updateWeeks();
    } catch (err) {
        error.value = "Failed to load lectures. Please try again.";
    } finally {
        isLoading.value = false;
    }
});

const emit = defineEmits(["toggleCreateLecture"]);
const toggleCreateLecture = () => {
    emit("toggleCreateLecture");
};

const openLectures = ref({});

const toggleLecture = (name) => {
    openLectures.value[name] = !openLectures.value[name];
};

const showCreateSubLecture = ref(false);
const toggleCreateSubLecture = (weekId) => {
    store.commit('course/SET_CREATING_WEEK', weekId);
    showCreateSubLecture.value = !showCreateSubLecture.value;
    updateWeeks();
};

const showAddLecture = ref(false);
const toggleAddLecture = () => {
    showAddLecture.value = !showAddLecture.value;
    updateWeeks();
};

// Edit lecture functionality
const editingLecture = ref(null);
const editLecture = (lecture) => {
    editingLecture.value = lecture;
    // Implementation for editing lecture would go here
    // For now, we'll just log it
    console.log("Editing lecture:", lecture);
    // In a real implementation, you might open a modal or form for editing
};

// Delete lecture functionality
const deleteLecture = async (lectureId) => {
    if (!confirm("Are you sure you want to delete this lecture? This action cannot be undone.")) {
        return;
    }
    
    isLoading.value = true;
    error.value = null;
    
    try {
        const courseId = creatingCourse.value.id;
        const response = await deleteWeekAPI(courseId, lectureId);
        
        if (response && response.status === 200) {
            await updateWeeks();
        } else {
            throw new Error(response?.data?.message || "Failed to delete lecture");
        }
    } catch (err) {
        error.value = err.message || "An error occurred while deleting the lecture";
    } finally {
        isLoading.value = false;
    }
};

// Delete sub-lecture (material) functionality
const deleteMaterial = async (weekId, materialId) => {
    if (!confirm("Are you sure you want to delete this content? This action cannot be undone.")) {
        return;
    }
    
    isLoading.value = true;
    error.value = null;
    
    try {
        const response = await deleteMaterialAPI(weekId, materialId);
        
        if (response && response.status === 200) {
            await updateWeeks();
        } else {
            throw new Error(response?.data?.message || "Failed to delete content");
        }
    } catch (err) {
        error.value = err.message || "An error occurred while deleting the content";
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
    <div class="flex justify-center items-center w-full h-full absolute top-0">
        <div class="w-[90%] h-[92vh] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4 overflow-auto">

            <div class="flex justify-end">
                <md-icon-button @click="toggleCreateLecture">
                    <md-icon>close</md-icon>
                </md-icon-button>
            </div>

            <div class="flex flex-col items-center justify-center h-full">
                <div class="w-[70%] mx-auto px-25 p-12 rounded-[12px] bg-(--md-sys-color-surface-container)">
                    <div class="flex justify-between items-center mb-6">
                        <span class="px-10 py-2 text-2xl font-bold">Course Lectures</span>
                    </div>

                    <!-- Loading state -->
                    <div v-if="isLoading" class="flex justify-center items-center py-10">
                        <md-circular-progress indeterminate></md-circular-progress>
                    </div>

                    <!-- Error message -->
                    <div v-if="error" class="bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) p-4 rounded-lg mb-4">
                        <div class="flex items-center gap-2">
                            <md-icon>error</md-icon>
                            <span>{{ error }}</span>
                        </div>
                    </div>

                    <!-- Empty state -->
                    <div v-if="!isLoading && (!lectures || lectures.length === 0)" class="flex flex-col items-center justify-center py-10 text-center">
                        <p class="text-xl mb-2">No lectures added yet</p>
                        <p class="text-(--md-sys-color-outline) mb-6">Start by adding your first lecture</p>

                    </div>

                    <!-- Lectures list -->
                    <div v-if="!isLoading && lectures && lectures.length > 0" class="space-y-4">
                        <div v-for="lecture in lectures" :key="lecture.id" class="mb-4">
                            <!-- Main lecture header -->
                            <md-list class="rounded-[12px] border border-(--md-sys-color-outline) overflow-hidden">
                                <md-list-item 
                                    @click="toggleLecture(lecture.name)" 
                                    class="cursor-pointer bg-(--md-sys-color-secondary-container) border-b border-(--md-sys-color-outline) px-5"
                                >
                                    <div slot="start">
                                        <md-icon>menu_book</md-icon>
                                    </div>
                                    <span class="font-medium">{{ lecture.name }}</span>
                                    <div slot="end" class="flex gap-2 items-center">
                                        <md-icon-button @click.stop="editLecture(lecture)">
                                            <md-icon>edit</md-icon>
                                        </md-icon-button>
                                        <md-icon-button @click.stop="deleteLecture(lecture.id)">
                                            <md-icon>delete</md-icon>
                                        </md-icon-button>
                                        <span class="text-xl">|</span>
                                        <md-icon>{{ openLectures[lecture.name] ? 'expand_less' : 'expand_more' }}</md-icon>
                                    </div>
                                </md-list-item>

                                <!-- Sub lectures dropdown -->
                                <div v-if="openLectures[lecture.name]" class="bg-(--md-sys-color-surface)">
                                    <!-- Empty state for sub-lectures -->
                                    <div v-if="!lecture.materials || lecture.materials.length === 0" class="py-6 px-4 text-center">
                                        <p class="text-(--md-sys-color-outline) mb-2">No content added to this lecture yet</p>
                                        <md-outlined-button class="mt-2 w-35" @click="toggleCreateSubLecture(lecture.id)">
                                            <md-icon slot="icon">add</md-icon>Add Content
                                        </md-outlined-button>
                                    </div>
                                    
                                    <!-- Sub-lectures list -->
                                    <div v-else>
                                        <md-list-item 
                                            v-for="material in lecture.materials" 
                                            :key="material.id"
                                            class="px-15 border-b border-(--md-sys-color-outline-variant)"
                                        >
                                            <div slot="start">
                                                <md-icon>description</md-icon>
                                            </div>
                                            <div class="flex flex-col">
                                                <span class="font-medium">{{ material.material_name }}</span>
                                                <span class="text-sm text-(--md-sys-color-outline)">Duration: {{ material.duration }} min</span>
                                            </div>
                                            <div slot="end" class="flex gap-2">
                                                <md-icon-button>
                                                    <md-icon>edit</md-icon>
                                                </md-icon-button>
                                                <md-icon-button @click.stop="deleteMaterial(lecture.id, material.id)">
                                                    <md-icon>delete</md-icon>
                                                </md-icon-button>
                                            </div>
                                        </md-list-item>
                                        <div class="flex justify-end">
                                            <md-outlined-button class="m-4 w-45 h-12" @click="toggleCreateSubLecture(lecture.id)">
                                                <md-icon slot="icon">add</md-icon>Add More Content
                                            </md-outlined-button>
                                        </div>
                                    </div>
                                </div>
                            </md-list>
                        </div>
                    </div>
                </div>
                <div class="flex justify-end w-[70%] mt-8 gap-5">
                    <md-filled-button class="w-35 h-12" @click="toggleAddLecture">
                        <md-icon slot="icon">add</md-icon>Add Lecture
                    </md-filled-button>
                    <md-filled-button class="w-30 h-12" @click="toggleCreateLecture">Save & Finish</md-filled-button>
                </div>
            </div>
        </div>
    </div>
    <CreateSubLectureView v-if="showCreateSubLecture" @toggleCreateSubLecture="toggleCreateSubLecture" />
    <CreateLecture v-if="showAddLecture" @toggleAddLecture="toggleAddLecture" />
</template>
