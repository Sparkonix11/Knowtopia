import { apiConnector } from "../apiConnector";
import { materialDoubtEndpoints } from "../apis";

const { CREATE_DOUBT, MATERIAL_DOUBTS, ALL_MATERIAL_DOUBTS, STUDENT_DOUBTS } = materialDoubtEndpoints;

// Create a new material doubt
export async function createMaterialDoubtAPI(materialId, doubtText) {
    try {
        const response = await apiConnector('POST', CREATE_DOUBT(materialId), { doubt_text: doubtText });
        return response;
    } catch (error) {
        console.error('Create material doubt error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

// Get all doubts for a specific material
export async function getMaterialDoubtsAPI(materialId) {
    try {
        const response = await apiConnector('GET', MATERIAL_DOUBTS(materialId));
        return response;
    } catch (error) {
        console.error('Get material doubts error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

// Get all material doubts for instructor's courses
export async function getAllMaterialDoubtsAPI() {
    try {
        const response = await apiConnector('GET', ALL_MATERIAL_DOUBTS);
        return response;
    } catch (error) {
        console.error('Get all material doubts error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

// Get student's doubts by day for the last 10 days
export async function getStudentDoubtsAPI() {
    try {
        const response = await apiConnector('GET', STUDENT_DOUBTS);
        return response;
    } catch (error) {
        console.error('Get student doubts error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}