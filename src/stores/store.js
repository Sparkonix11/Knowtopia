import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import user from "./user";
import course from "./course";

const store = createStore({
    modules: {
        user,
        course
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
