import { askAIAPI } from "../services/operations/aiAPI";

export default {
    namespaced: true,
    state: {
        conversations: {},
        currentMaterialId: null,
        isLoading: false,
        error: null
    },
    mutations: {
        SET_CURRENT_MATERIAL_ID(state, materialId) {
            state.currentMaterialId = materialId;
        },
        ADD_MESSAGE(state, { materialId, message, isUser }) {
            // Initialize conversation for this material if it doesn't exist
            if (!state.conversations[materialId]) {
                state.conversations[materialId] = [];
            }
            
            // Add the message to the conversation
            state.conversations[materialId].push({
                id: Date.now(), // Simple unique ID
                content: message,
                isUser: isUser,
                timestamp: new Date().toISOString()
            });
        },
        SET_LOADING(state, isLoading) {
            state.isLoading = isLoading;
        },
        SET_ERROR(state, error) {
            state.error = error;
        }
    },
    actions: {
        setCurrentMaterial({ commit }, materialId) {
            commit('SET_CURRENT_MATERIAL_ID', materialId);
        },
        async sendMessage({ commit, state }, message) {
            try {
                commit('SET_LOADING', true);
                commit('SET_ERROR', null);
                
                // Add user message to conversation
                const materialId = state.currentMaterialId || 'general';
                commit('ADD_MESSAGE', { materialId, message, isUser: true });
                
                // Send message to API
                const payload = {
                    question: message,
                    material_id: state.currentMaterialId
                };
                
                console.log('Sending payload:', payload);
const response = await askAIAPI(payload);
console.log('API response received:', response);
                
                // Clear message input by returning null to parent component
                if (response.status === 200) {
                    // Add AI response to conversation
                    commit('ADD_MESSAGE', { 
                        materialId, 
                        message: response.data.answer, 
                        isUser: false 
                    });
                } else {
                    commit('SET_ERROR', response.data?.error || 'Failed to get response from AI');
                }
            } catch (error) {
console.error('Full error object:', error);
console.log('Error response exists:', !!error.response);
                console.error('Error sending message:', error);
                commit('SET_ERROR', error.message || 'An error occurred while sending your message');
            } finally {
                commit('SET_LOADING', false);
            }
        }
    },
    getters: {
        getCurrentConversation: (state) => {
            const materialId = state.currentMaterialId || 'general';
            return state.conversations[materialId] || [];
        },
        isLoading: (state) => state.isLoading,
        error: (state) => state.error
    }
};