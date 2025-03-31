<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';

const props = defineProps({
    currentMaterialId: {
        type: [Number, String],
        default: null
    }
});

const store = useStore();
const message = ref('');


watch(() => message.value, (newValue) => {
  console.log('Message updated:', {
    value: newValue,
    trimmedLength: newValue.trim().length
  });
}, { immediate: false });
const isLoading = computed(() => store.getters['chat/isLoading']);
const error = computed(() => store.getters['chat/error']);
const conversation = computed(() => store.getters['chat/getCurrentConversation']);
const canSendMessage = computed(() => !isLoading.value && message.value.trim().length > 0);


watch(() => props.currentMaterialId, (newValue) => {
    if (newValue) {
        store.dispatch('chat/setCurrentMaterial', newValue);
    }
}, { immediate: true });

const sendMessage = async () => {
  console.log('Attempting to send message:', message.value.trim());
  if (!message.value.trim()) {
    console.warn('Send blocked - empty message');
    return;
  }
  
  try {
    const flatMessage = message.value.trim();
    console.log('Dispatching sendMessage action with:', flatMessage);
    await store.dispatch('chat/sendMessage', flatMessage);
    console.log('Message sent successfully');
    message.value = '';
    console.log('Message input reset');
  } catch (err) {
    console.error('Error sending message:', err);
  }
};

watch(isLoading, (newVal) => {
  console.log('Loading state changed:', newVal);
});


const chatContainer = ref(null);
watch(() => conversation.value.length, () => {
    setTimeout(() => {
        if (chatContainer.value) {
            chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
        }
    }, 100);
});
</script>

<template>
    <div class="flex flex-col h-[400px] w-full max-w-md bg-surface rounded-lg overflow-hidden">
        <div class="p-3 md:p-4 border-b border-outline-variant bg-surface-container">
            <h3 class="text-lg font-medium">AI Assistant</h3>
            <p class="text-sm text-gray-500">
                {{ props.currentMaterialId ? 'Discussing current material' : 'General assistance' }}
            </p>
        </div>
        
        <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
            <div v-if="conversation.length === 0" class="flex flex-col items-center justify-center h-full gap-3">
                <md-icon class="text-4xl text-gray-400">chat</md-icon>
                <p class="text-center text-gray-500">Ask me anything about your courses or materials!</p>
            </div>
            
            <div v-else v-for="msg in conversation" :key="msg.id" 
                 :class="['flex mb-2 max-w-[80%]', msg.isUser ? 'self-end' : 'self-start']">
                <div :class="['p-2 md:p-3 rounded-xl relative', 
                              msg.isUser ? 'bg-primary-container text-on-primary-container' : 
                                          'bg-secondary-container text-on-secondary-container']">
                    <p>{{ msg.content }}</p>
                    <span class="text-[0.7rem] opacity-70 block text-right mt-1">{{ new Date(msg.timestamp).toLocaleTimeString() }}</span>
                </div>
            </div>
            
            <div v-if="isLoading" class="self-center my-2">
                <md-circular-progress indeterminate></md-circular-progress>
            </div>
            
            <div v-if="error" class="text-error p-2 rounded-lg bg-error-container my-2">
                <p>{{ error }}</p>
            </div>
        </div>
        
        <div class="flex p-2 md:p-4 gap-2 border-t border-outline-variant bg-surface-container">
            <md-filled-text-field
                class="flex-1"
                :value="message"
                @input="message = $event.target.value"
                placeholder="Type your message..."
                @keyup.enter="sendMessage"
                :disabled="isLoading"
            ></md-filled-text-field>
            <md-filled-icon-button @click="sendMessage" :disabled="!canSendMessage">
                <md-icon>send</md-icon>
            </md-filled-icon-button>
        </div>
    </div>
</template>

<!-- No scoped styles needed as we're using Tailwind utility classes -->