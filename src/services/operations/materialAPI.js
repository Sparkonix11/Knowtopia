import { materialEndpoints } from "../apis";
import { apiConnector } from "../apiConnector";

const { CREATE_MATERIAL, DELETE_MATERIAL } = materialEndpoints;

export async function createMaterialAPI(weekId, formData) {
    try {
        const response = await apiConnector('POST', CREATE_MATERIAL(weekId), formData);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function deleteMaterialAPI(weekId, materialId) {
    try {
        const response = await apiConnector('DELETE', DELETE_MATERIAL(weekId, materialId));
        return response;
    } catch (error) {
        return error.response;
    }
}