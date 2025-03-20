import { getCourseAPI, getInstructorCoursesAPI, getEnrolledCoursesAPI } from '../services/operations/courseAPI';

export default {
    namespaced: true,
    state: {
        courses: [],
        enrolledCourses: [],
        instructorCourses: [],
        instructorLectures: []
    },
    mutations: {
        SET_COURSES(state, courses) {
            state.courses = courses;
        },
        SET_ENROLLED_COURSES(state, courses) {
            state.enrolledCourses = courses;
        },
        SET_INSTRUCTOR_COURSES(state, courses) {
            state.instructorCourses = courses;
        },
        SET_INSTRUCTOR_LECTURES(state, lectures) {
            state.instructorLectures = lectures;
        }
    },
    actions: {
        async updateCourses({ commit }) {
            try {
                const response = await getCourseAPI();
                if (response.status === 200) {
                    commit('SET_COURSES', response.data.courses);
                }
                return response;
            } catch (error) {
                return error.response;
            }
        },
        async updateEnrolledCourses({ commit }) {
            try {
                const response = await getEnrolledCoursesAPI();
                if (response.status === 200) {
                    commit('SET_ENROLLED_COURSES', response.data.courses);
                }
                return response;
            } catch (error) {
                return error.response;
            }
        },
        async updateInstructorCourses({ commit }) {
            try {
                const response = await getInstructorCoursesAPI();
                if (response.status === 200) {
                    commit('SET_INSTRUCTOR_COURSES', response.data.courses);
                }
                return response;
            } catch (error) {
                return error.response;
            }
        }
    },
    getters: {
        getCourses: (state) => state.courses,
        getEnrolledCourses: (state) => state.enrolledCourses,
        getInstructorCourses: (state) => state.instructorCourses,
        getInstructorLectures: (state) => state.instructorLectures
    }
};
