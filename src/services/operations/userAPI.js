import { apiConnector } from "../apiConnector";
import { userEndpoints } from "../apis";

const { USER_PROFILE, USER_STUDENT_LIST } = userEndpoints;

export async function getUserProfile() {
    try {
        const response = await apiConnector('GET', USER_PROFILE);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function updateUserProfile(formData) {
    try {
        const response = await apiConnector('PUT', USER_PROFILE, formData);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function getUserStudents() {
    try {
        const response = await apiConnector('GET', USER_STUDENT_LIST);
        return response;
    } catch (error) {
        return error.response;
    }
}
