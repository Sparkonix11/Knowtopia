import { weekEndpoints } from "../apis";
import { apiConnector } from "../apiConnector";

const { CREATE_WEEK, DELETE_WEEK } = weekEndpoints;

export async function createWeekAPI(courseId, formData) {
    try {
        const response = await apiConnector('POST', CREATE_WEEK(courseId), formData);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function deleteWeekAPI(courseId, weekId) {
    try {
        const response = await apiConnector('DELETE', DELETE_WEEK(courseId, weekId));
        return response;
    } catch (error) {
        return error.response;
    }
}