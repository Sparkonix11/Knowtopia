import pytest
import requests
from tests import ENDPOINTS

def test_create_review(student_session):
    """Test successfully creating a review for a material"""
    # Create a test material using form data
    material_data = {
        "title": "Test Material",
        "description": "Material for review testing"
    }
    material_create_response = student_session.post(
        ENDPOINTS["material_create"], 
        data=material_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert material_create_response.status_code == 201
    material_id = material_create_response.json()["material"]["id"]

    # Create a review using form data
    review_data = {
        "rating": "5",  # Send as string since form data is always strings
        "comment": "Excellent material!"
    }
    response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=review_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    # Verify response
    assert response.status_code == 201
    assert response.json()["message"] == "Review created"
    assert response.json()["review"]["rating"] == 5  # Check as integer since backend converts it
    assert response.json()["review"]["comment"] == "Excellent material!"
    assert response.json()["review"]["material_id"] == material_id
    assert "user_id" in response.json()["review"]

def test_create_review_missing_fields(student_session):
    """Test creating a review with missing fields"""
    # Create a test material
    material_data = {
        "title": "Material Missing Fields",
        "description": "Checking required fields"
    }
    material_create_response = student_session.post(
        ENDPOINTS["material_create"], 
        data=material_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert material_create_response.status_code == 201
    material_id = material_create_response.json()["material"]["id"]

    # Attempt to create review with missing comment field
    incomplete_data = {"rating": "4"}
    response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=incomplete_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Missing required fields"

def test_create_review_invalid_rating(student_session):
    """Test creating a review with an invalid rating"""
    # Create a test material
    material_data = {
        "title": "Material Invalid Rating",
        "description": "Checking rating validation"
    }
    material_create_response = student_session.post(
        ENDPOINTS["material_create"], 
        data=material_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert material_create_response.status_code == 201
    material_id = material_create_response.json()["material"]["id"]

    # Test rating too high
    high_rating_data = {
        "rating": "6",  # Above maximum
        "comment": "Too high rating"
    }
    response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=high_rating_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
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
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Rating must be between 1 and 5"

def test_create_review_duplicate(student_session):
    """Test creating a duplicate review by the same user"""
    # Create a test material
    material_data = {
        "title": "Material Duplicate Review",
        "description": "Checking duplicate review prevention"
    }
    material_create_response = student_session.post(
        ENDPOINTS["material_create"], 
        data=material_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert material_create_response.status_code == 201
    material_id = material_create_response.json()["material"]["id"]

    # Create first review
    review_data = {
        "rating": "4",
        "comment": "Great material!"
    }
    first_response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=review_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert first_response.status_code == 201
    
    # Attempt to create duplicate review
    duplicate_response = student_session.post(
        ENDPOINTS["review"].format(material_id=material_id), 
        data=review_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["error"] == "Review already exists"

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