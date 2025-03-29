from tests import ENDPOINTS
from tests.conftest import create_test_week, delete_test_week, create_test_assignment, delete_test_assignment

def test_create_assignment(instructor_session):
    """Test to create an assignment as an instructor"""
    course_id, week_id, assignment_id = create_test_assignment(instructor_session)
    delete_test_assignment(instructor_session, course_id, week_id, assignment_id)

def test_create_assignment_unauthorized(student_session, instructor_session):
    """Test for an unauthorized attempt to create an assignment"""
    course_id, week_id = create_test_week(instructor_session)
    data = {
        "name": "Fake Assignment",
        "description": "Assignment creation attempt by an unauthorized user"
    }
    response = student_session.post(ENDPOINTS["create_assignment"].format(week_id=week_id), data=data)
    assert response.status_code == 403
    assert response.json()["error"] == "Access denied. Only instructors can create assignments"
    delete_test_week(instructor_session, course_id, week_id)

def test_create_assignment_missing_fields(instructor_session):
    """Test to create an assignment with missing required fields"""
    course_id, week_id = create_test_week(instructor_session)
    data = {"name": "Assignment with missing fields"}
    response = instructor_session.post(ENDPOINTS["create_assignment"].format(week_id=week_id), data=data)
    assert response.status_code == 400
    assert response.json()["error"] == "Missing required fields"
    delete_test_week(instructor_session, course_id, week_id)

def test_create_assignment_invalid_week(instructor_session):
    """Test assignment creation for a non-existent week"""
    invalid_week_id = 9999  # Assuming this ID does not exist
    data = {
        "name": "Invalid Week Assignment",
        "description": "Testing assignment creation with invalid week"
    }
    response = instructor_session.post(ENDPOINTS["create_assignment"].format(week_id=invalid_week_id), data=data)
    assert response.status_code == 404
    assert response.json()["error"] == "Week not found"

def test_get_assignment(instructor_session):
    """Test retrieving an existing assignment"""
    course_id, week_id, assignment_id = create_test_assignment(instructor_session)
    response = instructor_session.get(ENDPOINTS["assignment"].format(assignment_id=assignment_id))
    assert response.status_code == 200, "Failed to retrieve assignment"
    json_response = response.json()
    assert "assignment" in json_response
    assert json_response["assignment"]["id"] == assignment_id
    delete_test_assignment(instructor_session, course_id, week_id, assignment_id)

def test_get_assignment_not_found(instructor_session):
    """Test retrieving an assignment that doesn't exist"""
    invalid_assignment_id = 9999  # Assuming this ID does not exist
    response = instructor_session.get(ENDPOINTS["assignment"].format(assignment_id=invalid_assignment_id))
    assert response.status_code == 404
    assert response.json()["error"] == "Assignment not found"

def test_delete_assignment(instructor_session):
    """Test deleting an existing assignment as an instructor"""
    course_id, week_id, assignment_id = create_test_assignment(instructor_session)
    delete_test_assignment(instructor_session, course_id, week_id, assignment_id)

def test_delete_assignment_not_found(instructor_session):
    """Test deleting an assignment that does not exist"""
    invalid_assignment_id = 9999  # Assuming this ID does not exist
    response = instructor_session.delete(ENDPOINTS["delete_assignment"].format(assignment_id=invalid_assignment_id))
    assert response.status_code == 404
    assert response.json()["error"] == "Assignment not found"

def test_delete_assignment_unauthorized(student_session, instructor_session):
    """Test unauthorized assignment deletion attempt"""
    course_id, week_id, assignment_id = create_test_assignment(instructor_session)
    response = student_session.delete(ENDPOINTS["delete_assignment"].format(assignment_id=assignment_id))
    assert response.status_code == 403
    assert response.json()["error"] == "Access denied. Only instructors can delete assignments"
    delete_test_assignment(instructor_session, course_id, week_id, assignment_id)
