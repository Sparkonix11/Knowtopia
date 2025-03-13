from tests import ENDPOINTS

def test_create_week(instructor_session):
    """Test instructor successfully creating a week"""
    course_data = {
        "name": "Test Course for Week Creation",
        "description": "A course to test week creation"
    }
    create_course_response = instructor_session.post(ENDPOINTS["create_course"], data=course_data)
    assert create_course_response.status_code == 201
    course_id = create_course_response.json()["course"]["id"]

    week_data = {"name": "Week 1"}
    response = instructor_session.post(ENDPOINTS["week_create"].format(course_id=course_id), data=week_data)
    assert response.status_code == 201
    assert response.json()["message"] == "Week created"

def test_create_week_unauthorized(student_session):
    """Test student attempting to create a week (should be unauthorized)"""
    response = student_session.post(ENDPOINTS["week_create"].format(course_id=1), data={"name": "Week 1"})
    assert response.status_code == 403
    assert response.json()["error"] == "User is not an instructor"

def test_create_week_missing_fields(instructor_session):
    """Test creating a week with missing required fields"""
    course_data = {
        "name": "Course for Week Test",
        "description": "Testing missing fields in week creation"
    }
    create_course_response = instructor_session.post(ENDPOINTS["create_course"], data=course_data)
    assert create_course_response.status_code == 201
    course_id = create_course_response.json()["course"]["id"]

    response = instructor_session.post(ENDPOINTS["week_create"].format(course_id=course_id), data={})
    assert response.status_code == 400
    assert response.json()["error"] == "Missing required fields"

def test_create_duplicate_week(instructor_session):
    """Test creating a week with a duplicate name"""
    course_data = {
        "name": "Course for Duplicate Week Test",
        "description": "Testing duplicate week creation"
    }
    create_course_response = instructor_session.post(ENDPOINTS["create_course"], data=course_data)
    assert create_course_response.status_code == 201
    course_id = create_course_response.json()["course"]["id"]

    week_data = {"name": "Week 1"}
    response1 = instructor_session.post(ENDPOINTS["week_create"].format(course_id=course_id), data=week_data)
    assert response1.status_code == 201

    response2 = instructor_session.post(ENDPOINTS["week_create"].format(course_id=course_id), data=week_data)
    assert response2.status_code == 400
    assert response2.json()["error"] == "Week already exists"

def test_delete_week(instructor_session):
    """Test instructor successfully deleting a week"""
    course_data = {
        "name": "Course for Week Deletion",
        "description": "Testing week deletion"
    }
    create_course_response = instructor_session.post(ENDPOINTS["create_course"], data=course_data)
    assert create_course_response.status_code == 201
    course_id = create_course_response.json()["course"]["id"]

    week_data = {"name": "Week to Delete"}
    create_week_response = instructor_session.post(ENDPOINTS["week_create"].format(course_id=course_id), data=week_data)
    assert create_week_response.status_code == 201
    week_id = create_week_response.json()["week"]["id"]

    delete_response = instructor_session.delete(ENDPOINTS["week_delete"].format(course_id=course_id, week_id=week_id))
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Week deleted"

def test_delete_week_unauthorized(student_session):
    """Test unauthorized user (student) attempting to delete a week"""
    response = student_session.delete(ENDPOINTS["week_delete"].format(course_id=1, week_id=1))
    assert response.status_code == 403
    assert response.json()["error"] == "User is not the creator of the course"

def test_delete_nonexistent_week(instructor_session):
    """Test deleting a non-existent week"""
    response = instructor_session.delete(ENDPOINTS["week_delete"].format(course_id=1, week_id=9999))
    assert response.status_code == 404
    assert response.json()["error"] == "Week not found"
