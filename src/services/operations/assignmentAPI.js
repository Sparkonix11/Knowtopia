import { apiConnector } from "../apiConnector";
import { assignmentEndpoints } from "../apis";

const { GET_ASSIGNMENT, CREATE_ASSIGNMENT, DELETE_ASSIGNMENT, SUBMIT_ASSIGNMENT, GET_ASSIGNMENT_SCORE } = assignmentEndpoints;

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

export async function submitAssignmentAPI(assignmentId, answers) {
    try {
        console.log('Submitting assignment:', assignmentId);
        const response = await apiConnector('POST', SUBMIT_ASSIGNMENT(assignmentId), { answers });
        console.log('Assignment submission response:', response);
        return response;
    } catch (error) {
        console.error('Assignment submission error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

export async function getAssignmentScoreAPI(assignmentId) {
    try {
        console.log('Fetching assignment score:', assignmentId);
        const response = await apiConnector('GET', GET_ASSIGNMENT_SCORE(assignmentId));
        console.log('Get assignment score response:', response);
        return response;
    } catch (error) {
        console.error('Get assignment score error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}