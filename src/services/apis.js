const SERVER_URL = 'http://127.0.0.1:5000';
const API_URL = `${SERVER_URL}/api/v1`;

export const authEndpoints = {
    LOGIN_API: `${API_URL}/auth/login`,
    SIGNUP_API: `${API_URL}/auth/signup`,
    LOGOUT_API: `${API_URL}/auth/logout`,
};

export const assignmentEndpoints = {
    GET_ASSIGNMENT: (assignmentId) => `${API_URL}/assignment/${assignmentId}`,
    CREATE_ASSIGNMENT: (weekId) => `${API_URL}/assignment/create/${weekId}`,
    DELETE_ASSIGNMENT: (assignmentId) => `${API_URL}/assignment/delete/${assignmentId}`,
    SUBMIT_ASSIGNMENT: (assignmentId) => `${API_URL}/assignment/submit/${assignmentId}`,
    GET_ASSIGNMENT_SCORE: (assignmentId) => `${API_URL}/assignment/score/${assignmentId}`,
    ALL_ASSIGNMENT_SCORES: `${API_URL}/assignment/all-scores`,
    ASSIGNMENT_SCORES: (assignmentId) => `${API_URL}/assignment/${assignmentId}/scores`,
};

export const courseEndpoints = {
    COURSE: `${API_URL}/course`,
    CREATE_COURSE: `${API_URL}/course/create`,
    INSTRUCTOR_COURSES: `${API_URL}/course/instructor`,
    DELETE_COURSE: (courseId) => `${API_URL}/course/delete/${courseId}`,
    EDIT_COURSE: (courseId) => `${API_URL}/course/edit/${courseId}`,
    ENROLLED_COURSES: `${API_URL}/course/enrolled`,
    ENROLL_STUDENT: (courseId, studentId) => `${API_URL}/course/enroll/${courseId}/${studentId}`,
    SINGLE_COURSE: (courseId) => `${API_URL}/course/${courseId}`,
};

export const enrollmentRequestEndpoints = {
    CREATE_REQUEST: `${API_URL}/enrollment-request`,
    STUDENT_REQUESTS: `${API_URL}/enrollment-request/student`,
    INSTRUCTOR_REQUESTS: `${API_URL}/enrollment-request/instructor`,
    REQUEST_ACTION: (requestId) => `${API_URL}/enrollment-request/${requestId}/action`,
};

export const materialEndpoints = {
    CREATE_MATERIAL: (weekId) => `${API_URL}/material/create/${weekId}`,
    DELETE_MATERIAL: (materialId) => `${API_URL}/material/delete/${materialId}`,
    EDIT_MATERIAL: (materialId) => `${API_URL}/material/edit/${materialId}`,
};

export const questionEndpoints = {
    CREATE_QUESTION: (assignmentId) => `${API_URL}/question/create/${assignmentId}`,
    LIST_QUESTIONS: (assignmentId) => `${API_URL}/question/${assignmentId}`,
    DELETE_QUESTION: (questionId) => `${API_URL}/question/delete/${questionId}`,
};

export const reviewEndpoints = {
    REVIEW: (materialId) => `${API_URL}/review/${materialId}`,
    DELETE_REVIEW: (reviewId) => `${API_URL}/review/delete/${reviewId}`,
    INSTRUCTOR_REVIEWS: `${API_URL}/review/instructor`,
};

export const userEndpoints = {
    USER_PROFILE: `${API_URL}/user`,
    USER_STUDENT_LIST: `${API_URL}/user/students`,
};

export const weekEndpoints = {
    CREATE_WEEK: (courseId) => `${API_URL}/week/create/${courseId}`,
    DELETE_WEEK: (courseId, weekId) => `${API_URL}/week/delete/${courseId}/${weekId}`,
    EDIT_WEEK: (courseId, weekId) => `${API_URL}/week/edit/${courseId}/${weekId}`,
};

export const aiEndpoints = {
    ASK: `${API_URL}/ask`,
    QUESTION_HINT: `${API_URL}/question_hint`,
    SUMMARIZE: `${API_URL}/summarize`,
};

export const searchEndpoints = {
    SEARCH: `${API_URL}/search`,
};

export const materialDoubtEndpoints = {
    CREATE_DOUBT: (materialId) => `${API_URL}/material/${materialId}/doubt`,
    MATERIAL_DOUBTS: (materialId) => `${API_URL}/material/${materialId}/doubts`,
    ALL_MATERIAL_DOUBTS: `${API_URL}/material/all-doubts`,
    STUDENT_DOUBTS: `${API_URL}/material/student-doubts`,
};
