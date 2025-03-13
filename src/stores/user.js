import { loginAPI, signupAPI, logoutAPI } from "../services/operations/authAPI";
import { updateUserProfile } from "../services/operations/userAPI";
export default {
    namespaced: true,
    state: {
        user: null,
        isAuth: false
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
            state.isAuth = true;
        },
        LOGOUT(state) {
            state.user = null;
            state.isAuth = false;
        }
    },
    actions: {
        async login({ commit }, formData) {
            try {
                const response = await loginAPI(formData);
                if (response.status === 200) {
                    commit('SET_USER', response.data.user);
                }
                return response;
            } catch (error) {    
                return error.response;
            }
        },
        async signup({ commit }, formData) {
            try {
                const response = await signupAPI(formData);
                if (response.status === 201) {
                    commit('SET_USER', response.data.user);
                }
                return response;
            } catch (error) {
                return error.response;
            }
        },
        async logout({ commit }) {
            try {
                const response = await logoutAPI();
                if (response.status === 200) {
                    commit('LOGOUT');
                }
                return response;
            } catch (error) {
                return error.response;
            }
        },
        async updateUserProfile({ commit }, formData) {
            try {
                const response = await updateUserProfile(formData);
                if (response.status === 200) {
                    commit('SET_USER', response.data.user);
                }
                return response;
            } catch (error) {
                return error.response;
            }
        },
    },
    getters: {
        currentUser: (state) => state.user,
        isAuthenticated: (state) => state.isAuth
    }
};