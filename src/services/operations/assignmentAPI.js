import { apiConnector } from "../apiConnector";
import { assignmentEndpoints } from "../apis";

const { GET_ASSIGNMENT, CREATE_ASSIGNMENT, DELETE_ASSIGNMENT } = assignmentEndpoints;

export async function getAssignmentAPI(assignmentId) {
    try {
        console.log('Fetching assignment:', assignmentId);
        const response = await apiConnector('GET', GET_ASSIGNMENT(assignmentId));
        console.log('Get assignment response:', response);
        return response;
    } catch (error) {
        console.error('Get assignment error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

export async function createAssignmentAPI(weekId, formData) {
    try {
        console.log('Creating assignment for week:', weekId);
        const response = await apiConnector('POST', CREATE_ASSIGNMENT(weekId), formData);
        console.log('Assignment creation response:', response);
        return response;
    } catch (error) {
        console.error('Assignment creation error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

export async function deleteAssignmentAPI(assignmentId) {
    try {
        console.log('Deleting assignment:', assignmentId);
        const response = await apiConnector('DELETE', DELETE_ASSIGNMENT(assignmentId));
        console.log('Delete assignment response:', response);
        return response;
    } catch (error) {
        console.error('Delete assignment error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}