from tests import ENDPOINTS

def test_create_question(instructor_session):
    """Test instructor successfully creating a question"""
    assignment_data = {
        "title": "Test Assignment",
        "description": "An assignment for testing question creation"
    }
    create_assignment_response = instructor_session.post(ENDPOINTS["create_assignment"], data=assignment_data)
    assert create_assignment_response.status_code == 201
    assignment_id = create_assignment_response.json()["assignment"]["id"]

    question_data = {
        "question_description": "What is 2 + 2?",
        "option1": "1",
        "option2": "2",
        "option3": "4",
        "option4": "5",
        "correct_option": "3"
    }
    response = instructor_session.post(ENDPOINTS["question_create"].format(assignment_id=assignment_id), data=question_data)
    assert response.status_code == 201
    assert response.json()["message"] == "Question created"

def test_create_question_unauthorized(student_session):
    """Test student attempting to create a question (should be unauthorized)"""
    response = student_session.post(ENDPOINTS["question_create"].format(assignment_id=1), data={
        "question_description": "Sample question?",
        "option1": "A",
        "option2": "B",
        "option3": "C",
        "option4": "D",
        "correct_option": "1"
    })
    assert response.status_code == 403
    assert response.json()["error"] == "Access denied. Only instructors can add questions."

def test_create_question_invalid_assignment(instructor_session):
    """Test creating a question with an invalid assignment_id"""
    response = instructor_session.post(ENDPOINTS["question_create"].format(assignment_id=9999), data={
        "question_description": "Invalid assignment question?",
        "option1": "A",
        "option2": "B",
        "option3": "C",
        "option4": "D",
        "correct_option": "1"
    })
    assert response.status_code == 404
    assert response.json()["error"] == "Invalid assignment_id"

def test_create_question_invalid_correct_option(instructor_session):
    """Test creating a question with an invalid correct_option"""
    assignment_data = {
        "title": "Assignment for Invalid Option Test",
        "description": "Checking incorrect correct_option"
    }
    create_assignment_response = instructor_session.post(ENDPOINTS["create_assignment"], data=assignment_data)
    assert create_assignment_response.status_code == 201
    assignment_id = create_assignment_response.json()["assignment"]["id"]

    response = instructor_session.post(ENDPOINTS["question_create"].format(assignment_id=assignment_id), data={
        "question_description": "Invalid correct option?",
        "option1": "A",
        "option2": "B",
        "option3": "C",
        "option4": "D",
        "correct_option": "5"
    })
    assert response.status_code == 400
    assert response.json()["error"] == "Correct option must be between 1 and 4"

def test_get_questions(instructor_session):
    """Test fetching all questions for an assignment"""
    assignment_data = {
        "title": "Assignment for Fetch Test",
        "description": "Checking question retrieval"
    }
    create_assignment_response = instructor_session.post(ENDPOINTS["create_assignment"], data=assignment_data)
    assert create_assignment_response.status_code == 201
    assignment_id = create_assignment_response.json()["assignment"]["id"]

    question_data = {
        "question_description": "What is the capital of France?",
        "option1": "Berlin",
        "option2": "Madrid",
        "option3": "Paris",
        "option4": "Rome",
        "correct_option": "3"
    }
    instructor_session.post(ENDPOINTS["question_create"].format(assignment_id=assignment_id), data=question_data)

    response = instructor_session.get(ENDPOINTS["question_list"].format(assignment_id=assignment_id))
    assert response.status_code == 200
    assert len(response.json()["questions"]) > 0

def test_get_questions_invalid_assignment(instructor_session):
    """Test fetching questions for an invalid assignment_id"""
    response = instructor_session.get(ENDPOINTS["question_list"].format(assignment_id=9999))
    assert response.status_code == 404
    assert response.json()["error"] == "Invalid assignment_id"

def test_delete_question(instructor_session):
    """Test instructor successfully deleting a question"""
    assignment_data = {
        "title": "Assignment for Question Deletion",
        "description": "Testing question deletion"
    }
    create_assignment_response = instructor_session.post(ENDPOINTS["create_assignment"], data=assignment_data)
    assert create_assignment_response.status_code == 201
    assignment_id = create_assignment_response.json()["assignment"]["id"]

    question_data = {
        "question_description": "What is 10 / 2?",
        "option1": "2",
        "option2": "5",
        "option3": "10",
        "option4": "20",
        "correct_option": "2"
    }
    create_question_response = instructor_session.post(ENDPOINTS["question_create"].format(assignment_id=assignment_id), data=question_data)
    assert create_question_response.status_code == 201
    question_id = create_question_response.json()["question"]["id"]

    delete_response = instructor_session.delete(ENDPOINTS["question_delete"].format(question_id=question_id))
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Question deleted"

def test_delete_question_unauthorized(student_session):
    """Test unauthorized user (student) attempting to delete a question"""
    response = student_session.delete(ENDPOINTS["question_delete"].format(question_id=1))
    assert response.status_code == 403
    assert response.json()["error"] == "Access denied. Only instructors can delete questions."

def test_delete_nonexistent_question(instructor_session):
    """Test deleting a non-existent question"""
    response = instructor_session.delete(ENDPOINTS["question_delete"].format(question_id=9999))
    assert response.status_code == 404
    assert response.json()["error"] == "Invalid question_id"
