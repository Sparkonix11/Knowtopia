import pytest
import requests
from tests import ENDPOINTS
from tests.conftest import create_test_course, delete_test_course

def test_get_all_courses():
    """Test retrieving all available courses"""
    response = requests.get(ENDPOINTS["course"])
    assert response.status_code == 200
    assert "courses" in response.json()

def test_get_instructor_courses(instructor_session):
    """Test retrieving courses created by the instructor"""
    response = instructor_session.get(ENDPOINTS["instructor_courses"])
    assert response.status_code == 200
    assert "courses" in response.json()

def test_create_course(instructor_session):
    """Test instructor creating a course"""
    course_id = create_test_course(instructor_session, "Instructor Course Test", 
                                  "A test course created by an instructor")
    delete_test_course(instructor_session, course_id)

def test_create_duplicate_course(instructor_session):
    """Test creating a course with a duplicate name"""
    course_name = "Duplicate Course Test"
    course_description = "This course will be tested for duplicates"
    
    # Create first course
    course_id = create_test_course(instructor_session, course_name, course_description)
    
    # Try to create duplicate
    course_data = {
        "name": course_name,
        "description": course_description
    }
    response = instructor_session.post(ENDPOINTS["create_course"], data=course_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Course already exists"
    
    # Clean up
    delete_test_course(instructor_session, course_id)

def test_create_course_missing_fields(instructor_session):
    """Test creating a course with missing required fields"""
    course_data = {"name": "Missing Description Test"}  # Missing description
    response = instructor_session.post(ENDPOINTS["create_course"], data=course_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Missing required fields"

def test_delete_course(instructor_session):
    """Test instructor deleting a course they created"""
    course_id = create_test_course(instructor_session, "Course to Delete", 
                                  "This course will be deleted")
    delete_test_course(instructor_session, course_id)

def test_delete_course_unauthorized(student_session, instructor_session):
    """Test unauthorized student trying to delete a course"""
    course_name = "Unauthorized Course Test"
    course_description = "This course will be tested for unauthorized course deletion"
    
    course_id = create_test_course(instructor_session, course_name, course_description)
    response = student_session.delete(ENDPOINTS["delete_course"].format(course_id=course_id))
    assert response.status_code == 403
    assert response.json()["error"] == "User is not an instructor"
    delete_test_course(instructor_session, course_id)

def test_get_enrolled_courses(student_session):
    """Test retrieving courses a student is enrolled in"""
    response = student_session.get(ENDPOINTS["enrolled_courses"])
    assert response.status_code == 200
    assert "enrolled_courses" in response.json()

def test_enroll_student(instructor_session):
    """Test instructor enrolling a student in their course"""
    student_id = 2  # Ensure this student exists
    
    # Create a course for testing enrollment
    course_id = create_test_course(instructor_session, "Enrollment Test Course", 
                                  "Course for testing enrollment")
    
    # Enroll the student
    enroll_response = instructor_session.post(
        ENDPOINTS["enroll_student"].format(course_id=course_id, student_id=student_id)
    )
    assert enroll_response.status_code == 201
    assert enroll_response.json()["message"] == "Student enrolled successfully"
    
    # Clean up
    delete_test_course(instructor_session, course_id)

def test_enroll_student_unauthorized(student_session):
    """Test student trying to enroll another student (unauthorized)"""
    response = student_session.post(
        ENDPOINTS["enroll_student"].format(course_id=1, student_id=2)
    )
    assert response.status_code == 403
    assert response.json()["error"] == "Only instructors can enroll students"