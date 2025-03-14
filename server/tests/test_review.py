import requests
from tests import ENDPOINTS
from tests.conftest import create_test_review, delete_test_review, create_test_material, delete_test_material

def test_create_review(instructor_session, student_session):
    """Test successfully creating a review for a material"""
    # Create a test material using form data
    course_id, week_id, material_id, review_id = create_test_review(instructor_session, student_session)
    delete_test_review(instructor_session, student_session, course_id, week_id, material_id, review_id)

def test_create_review_missing_fields(student_session, instructor_session):
    """Test creating a review with missing fields"""
    # Create a test material
    course_id, week_id, material_id = create_test_material(instructor_session)

    # Attempt to create review with missing comment field
    incomplete_data = {"rating": "4"}
    response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=incomplete_data
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Missing required fields"
    delete_test_material(instructor_session, course_id, week_id, material_id)

def test_create_review_invalid_rating(student_session, instructor_session):
    """Test creating a review with an invalid rating"""
    course_id, week_id, material_id = create_test_material(instructor_session)

    # Test rating too high
    high_rating_data = {
        "rating": "6",  # Above maximum
        "comment": "Too high rating"
    }
    response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=high_rating_data
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Rating must be between 1 and 5"
    
    # Test rating too low
    low_rating_data = {
        "rating": "0",  # Below minimum
        "comment": "Too low rating"
    }
    response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=low_rating_data,
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Rating must be between 1 and 5"
    delete_test_material(instructor_session, course_id, week_id, material_id)

def test_create_review_duplicate(student_session, instructor_session):
    """Test creating a duplicate review by the same user"""
    # Create a test material
    course_id, week_id, material_id, review_id = create_test_review(instructor_session, student_session)

    # Create first review
    review_data = {
        "rating": "4",
        "comment": "Great material!"
    }
    # Attempt to create duplicate review
    duplicate_response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=review_data
    )
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["error"] == "Review already exists"
    delete_test_review(instructor_session, student_session, course_id, week_id, material_id, review_id)

def test_create_review_nonexistent_material(student_session):
    """Test creating a review for a non-existent material"""
    # Attempt to create review for non-existent material ID
    review_data = {
        "rating": "3",
        "comment": "Testing invalid material"
    }
    response = student_session.post(
        ENDPOINTS["review"].format(material_id=9999), 
        data=review_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 404
    assert response.json()["error"] == "Material not found"

def test_create_review_unauthenticated():
    """Test creating a review without authentication"""
    # Attempt to create review without being logged in
    review_data = {
        "rating": "5",
        "comment": "Unauthorized review attempt"
    }
    # Using requests instead of student_session to simulate unauthenticated request
    response = requests.post(
        ENDPOINTS["review"].format(material_id=1), 
        data=review_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401  # Unauthorized