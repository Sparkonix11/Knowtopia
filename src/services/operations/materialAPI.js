import { materialEndpoints } from "../apis";
import { apiConnector } from "../apiConnector";

const { CREATE_MATERIAL, DELETE_MATERIAL, EDIT_MATERIAL, GET_MATERIAL } = materialEndpoints;

export async function createMaterialAPI(weekId, formData) {
    try {
        const response = await apiConnector('POST', CREATE_MATERIAL(weekId), formData);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function deleteMaterialAPI(materialId) {
    try {
        const response = await apiConnector('DELETE', DELETE_MATERIAL(materialId));
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function editMaterialAPI(materialId, formData) {
    try {
        const response = await apiConnector('PUT', EDIT_MATERIAL(materialId), formData);
        return response;
    } catch (error) {
        return error.response;
    }
}

export async function getMaterialAPI(materialId) {
    try {
        const response = await apiConnector('GET', GET_MATERIAL(materialId));
        return response;
    } catch (error) {
        return error.response;
    }
}