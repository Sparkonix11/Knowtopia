import { apiConnector } from "../apiConnector";
import { assignmentEndpoints } from "../apis";

const { ALL_ASSIGNMENT_SCORES, ASSIGNMENT_SCORES } = assignmentEndpoints;

// Get all assignment scores for instructor's courses
export async function getAllAssignmentScoresAPI() {
    try {
        const response = await apiConnector('GET', ALL_ASSIGNMENT_SCORES);
        return response;
    } catch (error) {
        console.error('Get all assignment scores error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

// Get scores for a specific assignment
export async function getAssignmentScoresAPI(assignmentId) {
    try {
        const response = await apiConnector('GET', ASSIGNMENT_SCORES(assignmentId));
        return response;
    } catch (error) {
        console.error('Get assignment scores error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}