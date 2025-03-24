import { apiConnector } from "../apiConnector";
import { aiEndpoints } from "../apis";

const { ASK, QUESTION_HINT } = aiEndpoints;

export async function getQuestionHintAPI(questionId) {
    try {
        console.log('Fetching hint for question:', questionId);
        const response = await apiConnector('POST', QUESTION_HINT, { question_id: questionId });
        console.log('Question hint response:', response);
        return response;
    } catch (error) {
        console.error('Question hint error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}

export async function askAIAPI(question) {
    try {
        console.log('Asking AI:', question);
        const response = await apiConnector('POST', ASK, { question });
        console.log('AI response:', response);
        return response;
    } catch (error) {
        console.error('AI ask error:', error);
        return error.response || { status: 500, data: { error: 'Network error or server not responding' } };
    }
}