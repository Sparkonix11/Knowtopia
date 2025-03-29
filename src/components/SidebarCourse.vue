<script setup>
import { defineProps, defineEmits, ref, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const props = defineProps({
  lectures: {
    type: Array,
    required: true,
    default: () => []
  },
  courseName: {
    type: String,
    default: 'Course Name'
  },
  courseId: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['select-material', 'edit-lecture', 'edit-sublecture', 'delete-lecture', 'delete-sublecture']);

const openLectures = ref({});
const isInstructor = computed(() => store.getters['user/currentUser']?.is_instructor);

const toggleLecture = (name) => {
  openLectures.value[name] = !openLectures.value[name];
};

const selectMaterial = (material) => {
  emit('select-material', material);
};

const editLecture = (lectureId, event) => {
  event.stopPropagation();
  emit('edit-lecture', lectureId);
};

const editSubLecture = (materialId, weekId, event) => {
  event.stopPropagation();
  emit('edit-sublecture', materialId, weekId);
};

const deleteLecture = (lectureId, event) => {
  event.stopPropagation();
  if (confirm('Are you sure you want to delete this lecture? This action cannot be undone.')) {
    emit('delete-lecture', lectureId);
  }
};

const deleteSubLecture = (materialId, weekId, event) => {
  event.stopPropagation();
  if (confirm('Are you sure you want to delete this content? This action cannot be undone.')) {
    emit('delete-sublecture', materialId, weekId);
  }
};
</script>
<template>
    <div class="w-[20%] h-[calc(100vh-5rem)] px-3 rounded-[12px] bg-(--md-sys-color-surface-container-low) overflow-y-auto fixed left-0 z-10">
        <span class="px-4 py-8 block text-xl">{{ courseName }}</span>

        <!-- Empty state -->
        <div v-if="!lectures || lectures.length === 0" class="flex flex-col items-center justify-center py-10 text-center">
            <p class="text-sm mb-2">No lectures available</p>
        </div>

        <div v-else v-for="lecture in lectures" :key="lecture.id || lecture.name">
            <!-- Main lecture header -->
            <md-list class="rounded-[50px] border-1 border-(--md-sys-color-outline) mb-3">
                <md-list-item @click="toggleLecture(lecture.name)" class="cursor-pointer bg-(--md-sys-color-secondary-container) rounded-[100px] border-(--md-sys-color-outline) border-b-1 px-2">
                    <div slot="start">
                        <md-icon>menu_book</md-icon>
                    </div>
                    <span class="font-medium">{{ lecture.name }}</span>

                    <div slot="end" class="flex gap-2 items-center">
                        <md-icon-button v-if="isInstructor" @click="editLecture(lecture.id, $event)" class="text-(--md-sys-color-on-secondary-container)">
                            <md-icon>edit</md-icon>
                        </md-icon-button>
                        <md-icon-button v-if="isInstructor" @click="deleteLecture(lecture.id, $event)" class="text-(--md-sys-color-error)">
                            <md-icon>delete</md-icon>
                        </md-icon-button>
                        <md-icon>{{ openLectures[lecture.name] ? 'expand_less' : 'expand_more' }}</md-icon>
                    </div>
                </md-list-item>

                <!-- Sub lectures dropdown -->
                <div v-if="openLectures[lecture.name]" class="rounded-[50px]">
                    <!-- Empty state for sublectures -->
                    <div v-if="!lecture.subLectures || lecture.subLectures.length === 0" class="py-3 px-6 text-center">
                        <p class="text-sm text-(--md-sys-color-outline)">No content in this lecture</p>
                    </div>
                    
                    <md-list-item 
                        v-else
                        v-for="subLecture in lecture.subLectures" 
                        :key="subLecture.id || subLecture"
                        :class="[
                            'rounded-[100px] px-6 border-b border-(--md-sys-color-outline-variant) hover:bg-(--md-sys-color-on-surface2)',
                            {'bg-(--md-sys-color-tertiary-container) text-(--md-sys-color-on-tertiary-container)': typeof subLecture === 'object' && subLecture.isAssignment}
                        ]"
                        @click="selectMaterial(subLecture)"
                    >
                        <div class="flex items-center gap-3 cursor-pointer w-full">
                            <!-- Show different icon based on material type -->
                            <div v-if="typeof subLecture === 'object' && subLecture.isAssignment">
                                <md-icon class="text-(--md-sys-color-on-tertiary-container)">assignment</md-icon>
                            </div>
                            <md-checkbox v-else touch-target="wrapper"></md-checkbox>
                            <span>{{ typeof subLecture === 'string' ? subLecture : subLecture.name }}</span>
                            <span v-if="typeof subLecture === 'object' && subLecture.isAssignment" class="text-xs ml-auto font-medium">Assignment</span>
                            
                            <!-- Edit and delete buttons for instructors -->
                            <div v-if="isInstructor && typeof subLecture === 'object' && subLecture.id" class="ml-auto flex gap-1">
                                <md-icon-button 
                                    @click="editSubLecture(subLecture.id, lecture.id, $event)" 
                                    class="text-(--md-sys-color-on-surface-variant)"
                                >
                                    <md-icon>edit</md-icon>
                                </md-icon-button>
                                <md-icon-button 
                                    @click="deleteSubLecture(subLecture.id, lecture.id, $event)" 
                                    class="text-(--md-sys-color-error)"
                                >
                                    <md-icon>delete</md-icon>
                                </md-icon-button>
                            </div>
                        </div>
                    </md-list-item>
                </div>
            </md-list>
        </div>
    </div>
</template>