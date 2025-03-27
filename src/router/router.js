import { createRouter, createWebHistory } from "vue-router";
import SignupView from "@/views/SignupView.vue";
import LoginView from "@/views/LoginView.vue";
import EnrolledCoursesView from "@/views/EnrolledCoursesView.vue";
import InstructorCoursesView from "@/views/InstructorCoursesView.vue";
import CourseView from "@/views/CourseVIew.vue";
import AssignmentView from "@/views/AssignmentView.vue";
import AssignmentReportView from "@/views/AssignmentReportView.vue";
import InstructorDashoard from "@/views/InstructorDashoard.vue";
import ProfileView from "@/views/ProfileView.vue";
import StudentDashboard from "@/views/StudentDashboard.vue";
import InstructorEnrollStudentsView from "@/views/InstructorEnrollStudentsView.vue";
import CreateAssignmentView from "@/views/CreateAssignmentView.vue";
import AssignmentsView from "@/views/AssignmentsView.vue";
import SearchResultsView from "@/views/SearchResultsView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            redirect: "/login"
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
        },
        {
            path: '/instructor-courses',
            name: 'InstructorCourses',
            component: InstructorCoursesView
        },
        {
            path: '/course/:id?',
            name: 'Course',
            component: CourseView
        },
        // {
        //     path: '/assignment',
        //     name: 'Assignment',
        //     component: AssignmentView
        // },
        {
            path: '/assignment-report',
            name: 'AssignmentReport',
            component: AssignmentReportView
        },
        {
            path: '/instructor-dashboard',
            name: 'InstructorDashboard',
            component: InstructorDashoard
        },
        {
            path: '/profile',
            name: 'Profile',
            component: ProfileView
        },
        {
            path: '/student-dashboard',
            name: 'StudentDashboard',
            component: StudentDashboard
        },
        {
            path: '/instructor-enroll',
            name: 'InstructorEnroll',
            component: InstructorEnrollStudentsView
        },
        {
            path: '/create-assignment',
            name: 'CreateAssignment',
            component: CreateAssignmentView
        },
        {
            path: '/assignments',
            name: 'Assignments',
            component: AssignmentsView
        },
        {
            path: '/search',
            name: 'SearchResults',
            component: SearchResultsView
        }
    ]
});

export default router;