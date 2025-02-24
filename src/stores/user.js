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
};