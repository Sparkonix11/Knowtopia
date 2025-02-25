import { apiConnector } from "../apiConnector";
import { authEndpoints } from "../apis";

const { LOGIN_API, SIGNUP_API, LOGOUT_API } = authEndpoints;

export async function loginAPI(formData) {
    try {
        const response = await apiConnector('POST', LOGIN_API, formData);
        return response;
    } catch (error) {      
        return error.response;
    }
}

export async function signupAPI(formData) {
    try {
        const response = await apiConnector('POST', SIGNUP_API, formData);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function logoutAPI() {
    try {
        const response = await apiConnector('POST', LOGOUT_API);
        return response;
    } catch (error) {
        return error.response;
    }
}