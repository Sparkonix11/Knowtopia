import { createRouter, createWebHistory } from "vue-router";
import SignupView from "@/views/SignupView.vue";
import LoginView from "@/views/LoginView.vue";
import EnrolledCoursesView from "@/views/EnrolledCoursesView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            redirect: "/signup"
        },
        {
            path: '/signup',
            name: 'Signup',
            component: SignupView
        },
        {
            path: '/login',
            name: 'Login',
            component: LoginView
        },
        {
            path: '/courses',
            name: 'EnrolledCourses',
            component: EnrolledCoursesView
        }
    ]
});
export default router;