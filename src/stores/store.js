import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import user from "./user";

const store = createStore({
    modules: {
        user
    },
    plugins: [
        createPersistedState({
            key: "my-app",
            paths: ["user"],
            storage: window.localStorage,
        })
    ]
});

export default store;
