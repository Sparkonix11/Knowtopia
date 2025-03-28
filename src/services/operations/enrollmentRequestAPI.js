import { apiConnector } from "../apiConnector";
import { enrollmentRequestEndpoints } from "../apis";

const { CREATE_REQUEST, STUDENT_REQUESTS, INSTRUCTOR_REQUESTS, REQUEST_ACTION } = enrollmentRequestEndpoints;

export async function createEnrollmentRequestAPI(courseId, message = "") {
    try {
        const response = await apiConnector('POST', CREATE_REQUEST, { course_id: courseId, message });
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function getStudentEnrollmentRequestsAPI() {
    try {
        const response = await apiConnector('GET', STUDENT_REQUESTS);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function getInstructorEnrollmentRequestsAPI() {
    try {
        const response = await apiConnector('GET', INSTRUCTOR_REQUESTS);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function processEnrollmentRequestAPI(requestId, action) {
    try {
        const response = await apiConnector('POST', REQUEST_ACTION(requestId), { action });
        return response;
    } catch (error) {
        return error.response;
    }
}