const SERVER_URL = 'http://127.0.0.1:5000';
const API_URL = `${SERVER_URL}/api/v1`;

export const authEndpoints = {
    LOGIN_API: `${API_URL}/auth/login`,
    SIGNUP_API: `${API_URL}/auth/signup`,
    LOGOUT_API: `${API_URL}/auth/logout`,
}