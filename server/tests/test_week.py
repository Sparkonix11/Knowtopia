from tests import ENDPOINTS
from tests.conftest import create_test_course, delete_test_course, create_test_week, delete_test_week

def test_create_week(instructor_session):
    """Test instructor successfully creating a week"""
    course_id, week_id = create_test_week(instructor_session)
    delete_test_week(instructor_session, course_id, week_id)

def test_create_week_unauthorized(student_session):
    """Test student attempting to create a week (should be unauthorized)"""
    response = student_session.post(ENDPOINTS["week_create"].format(course_id=1), data={"name": "Week 1"})
    assert response.status_code == 403
    assert response.json()["error"] == "User is not an instructor"

def test_create_week_missing_fields(instructor_session):
    """Test creating a week with missing required fields"""
    course_id = create_test_course(instructor_session, "Test Course for Week Creation", 
                                  "Testing missing fields in week creation")

    response = instructor_session.post(ENDPOINTS["week_create"].format(course_id=course_id), data={})
    assert response.status_code == 400
    assert response.json()["error"] == "Missing required fields"
    
    delete_test_course(instructor_session, course_id)

# def test_create_duplicate_week(instructor_session):
#     """Test creating a week with a duplicate name"""
#     course_id = create_test_course(instructor_session, "Test Course for Week Creation", 
#                                   "Testing duplicate week creation")

#     week_data = {"name": "Week 1"}
#     response1 = instructor_session.post(ENDPOINTS["week_create"].format(course_id=course_id), data=week_data)
#     assert response1.status_code == 201

#     response2 = instructor_session.post(ENDPOINTS["week_create"].format(course_id=course_id), data=week_data)
#     assert response2.status_code == 400
#     assert response2.json()["error"] == "Week already exists"

#     delete_test_course(instructor_session, course_id)

def test_delete_week(instructor_session):
    """Test instructor successfully deleting a week"""
    course_id, week_id = create_test_week(instructor_session)
    delete_test_week(instructor_session, course_id, week_id)

def test_delete_week_unauthorized(student_session, instructor_session):
    """Test unauthorized user (student) attempting to delete a week"""
    course_id, week_id = create_test_week(instructor_session)

    response = student_session.delete(ENDPOINTS["week_delete"].format(course_id=course_id, week_id=week_id))
    assert response.status_code == 403
    assert response.json()["error"] == "User is not the creator of the course"
    delete_test_week(instructor_session, course_id, week_id)

def test_delete_nonexistent_week(instructor_session):
    """Test deleting a non-existent week"""
    course_id = create_test_course(instructor_session, "Test Course for Week Creation", 
                                  "Testing non existent week deletion")
    response = instructor_session.delete(ENDPOINTS["week_delete"].format(course_id=course_id, week_id=9999))
    assert response.status_code == 404
    assert response.json()["error"] == "Week not found"
    
    delete_test_course(instructor_session, course_id)
