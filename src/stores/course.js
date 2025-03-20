import { getCourseAPI, getInstructorCoursesAPI, getEnrolledCoursesAPI } from '../services/operations/courseAPI';

export default {
    namespaced: true,
    state: {
        courses: [],
        enrolledCourses: [],
        instructorCourses: [],
        creatingCourse: null,
        creatingWeek: null,
        creatingCourseWeeks: [],
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
        },
        SET_CREATING_COURSE(state, course) {
            state.creatingCourse = course;
            state.creatingCourseWeeks = [];
        },
        SET_CREATING_WEEK(state, week) {
            state.creatingWeek = week;
        },
        SET_CREATING_COURSE_WEEKS(state, weeks) {
            state.creatingCourseWeeks = [...weeks];
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
        async updateInstructorCourses({ commit, state }) {
            try {
                const response = await getInstructorCoursesAPI();
                if (response.status === 200) {
                    commit('SET_INSTRUCTOR_COURSES', response.data.courses);

                    if (state.creatingCourse) {
                        const creatingCourseId = state.creatingCourse.id;
                        const courseData = response.data.courses.find(course => course.id === creatingCourseId);
                        commit('SET_CREATING_COURSE_WEEKS', courseData ? courseData.weeks : []);
                    }
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
        getCreatingCourse: (state) => state.creatingCourse,
        getCreatingWeek: (state) => state.creatingWeek,
        getCreatingCourseWeeks: (state) => state.creatingCourseWeeks,
    }
};
