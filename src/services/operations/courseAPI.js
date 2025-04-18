import { apiConnector } from "../apiConnector";
import { courseEndpoints } from "../apis";

const { COURSE, CREATE_COURSE, INSTRUCTOR_COURSES, DELETE_COURSE, EDIT_COURSE, ENROLLED_COURSES, ENROLL_STUDENT, SINGLE_COURSE } = courseEndpoints;

export async function createCourseAPI(formData) {
    try {
        const response = await apiConnector('POST', CREATE_COURSE, formData);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function getCourseAPI() {
    try {
        const response = await apiConnector('GET', COURSE);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function getInstructorCoursesAPI() {
    try {
        const response = await apiConnector('GET', INSTRUCTOR_COURSES);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function deleteCourseAPI(courseId) {
    try {
        const response = await apiConnector('DELETE', DELETE_COURSE(courseId));
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function editCourseAPI(courseId, formData) {
    try {
        const response = await apiConnector('PUT', EDIT_COURSE(courseId), formData);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function getEnrolledCoursesAPI() {
    try {
        const response = await apiConnector('GET', ENROLLED_COURSES);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function enrollStudentAPI(courseId, studentId) {
    try {
        const response = await apiConnector('POST', ENROLL_STUDENT(courseId, studentId));
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function getSingleCourseAPI(courseId) {
    try {
        const response = await apiConnector('GET', SINGLE_COURSE(courseId));
        return response;
    } catch (error) {
        return error.response;
    }
}