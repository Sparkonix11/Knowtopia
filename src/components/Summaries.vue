<script setup>
import { ref, onMounted } from 'vue';
import { getSummarizeAPI } from '@/services/operations/aiAPI';

const props = defineProps({
    materialId: {
        type: String,
        required: true
    }
});

const emit = defineEmits(["toggleSummaries"]);
const toggleSummaries = () => {
    emit("toggleSummaries");
};

const summary = ref('');
const topic = ref('');
const materialName = ref('');
const isLoading = ref(false);
const error = ref(null);

onMounted(async () => {
    try {
        isLoading.value = true;
        error.value = null;
        
        const response = await getSummarizeAPI(props.materialId);
        
        if (response.status === 200) {
            summary.value = response.data.summary;
            topic.value = response.data.topic;
            materialName.value = response.data.material_name;
        } else {
            error.value = response.data.error || 'Failed to get summary';
        }
    } catch (err) {
        console.error('Error fetching summary:', err);
        error.value = err.message || 'An error occurred while fetching the summary';
    } finally {
        isLoading.value = false;
    }
});
</script>

<template>
        <div class="flex justify-center items-center w-full h-full absolute top-0">
            <div class="w-[50%] h-[50vh] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4">
                <div class="flex justify-end">
                    <md-icon-button @click="toggleSummaries">
                        <md-icon>close</md-icon>
                    </md-icon-button>
                </div>

                <div class="flex flex-col text-justify w-[90%] m-auto gap-6 items-center justify-center h-[80%] overflow-y-auto">
                    <!-- Loading state -->
                    <div v-if="isLoading" class="flex justify-center items-center h-full w-full">
                        <md-circular-progress indeterminate></md-circular-progress>
                    </div>
                    
                    <!-- Error state -->
                    <div v-else-if="error" class="bg-(--md-sys-color-error-container) text-(--md-sys-color-on-error-container) p-4 rounded-lg mb-4 w-full">
                        <div class="flex items-center gap-2">
                            <md-icon>error</md-icon>
                            <span>{{ error }}</span>
                        </div>
                    </div>
                    
                    <!-- Summary content -->
                    <template v-else>
                        <span class="text-3xl text-center">{{ materialName }}</span>
                        <span class="text-xl text-center text-(--md-sys-color-primary)">{{ topic }}</span>
                        <div class="w-full">
                            <span v-html="summary.replace(/\n/g, '<br>')" class="whitespace-pre-line"></span>
                        </div>
                    </template>
                </div>
            </div>
        </div>
</template>