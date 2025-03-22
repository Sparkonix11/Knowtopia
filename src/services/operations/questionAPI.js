import { apiConnector } from "../apiConnector";
import { questionEndpoints } from "../apis";

const { CREATE_QUESTION, LIST_QUESTIONS, DELETE_QUESTION } = questionEndpoints;

export async function createQuestionAPI(assignmentId, formData) {
    try {
        console.log('Sending question creation request:', CREATE_QUESTION(assignmentId));
        const response = await apiConnector('POST', CREATE_QUESTION(assignmentId), formData);
        console.log('Question creation response:', response);
        return response;
    } catch (error) {
        console.error('Question creation error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

export async function listQuestionsAPI(assignmentId) {
    try {
        console.log('Fetching questions for assignment:', assignmentId);
        const response = await apiConnector('GET', LIST_QUESTIONS(assignmentId));
        console.log('List questions response:', response);
        return response;
    } catch (error) {
        console.error('List questions error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

export async function deleteQuestionAPI(questionId) {
    try {
        console.log('Deleting question:', questionId);
        const response = await apiConnector('DELETE', DELETE_QUESTION(questionId));
        console.log('Delete question response:', response);
        return response;
    } catch (error) {
        console.error('Delete question error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}