import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import user from "./user";
import course from "./course";
import chat from "./chat";

const store = createStore({
    modules: {
        user,
        course,
        chat
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
