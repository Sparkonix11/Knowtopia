import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/auth"  

@pytest.fixture
def valid_user():
    return {
        "email": "dummyuser@ds.study.iitm.ac.in",
        "password": "dummyPass@1",
        "password_confirm": "dummyPass@1",
        "fname": "Dummy",
        "lname": "User"
    }

def test_signup_success(valid_user):
    #Test for successful user registration
    response = requests.post(f"{BASE_URL}/signup", data=valid_user)
    assert response.status_code == 201
    assert response.json()["message"] == "User created"

def test_signup_password_mismatch():
    #Test registration fails when passwords do not match
    user_data = {
        "email": "dummyuser@ds.study.iitm.ac.in",
        "password": "dummyPass@1",
        "password_confirm": "dumPass@111",
        "fname": "Dummy",
        "lname": "User"
    }
    response = requests.post(f"{BASE_URL}/signup", data=user_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Passwords do not match"

def test_signup_missing_fields():
    #Test registration fails for required field missing
    user_data = {
        "email": "dummyuser@ds.study.iitm.ac.in",
        "password": "dummyPass@1",
        "password_confirm": "dummyPass@1",
        "fname": "Dummy"
        #Missing 'lname'
    }
    response = requests.post(f"{BASE_URL}/signup", data=user_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Missing required fields"
    print(response.json())

def test_signup_existing_user(valid_user):
    #Test registration fails for an existing user
    #user is registered first
    requests.post(f"{BASE_URL}/signup", data=valid_user)
    #Trying to register again with the same email
    response = requests.post(f"{BASE_URL}/signup", data=valid_user)
    assert response.status_code == 400
    assert response.json()["error"] == "User already exists"

def test_login_success():
    #Test for successful user login
    login_data = {
        "email": "dummyuser@ds.study.iitm.ac.in",
        "password": "dummyPass@1"
    }
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    assert response.status_code == 200
    assert response.json()["message"] == "User logged in"

def test_login_invalid_credentials():
    #Test login fails with wrong password
    login_data = {
        "email": "dummyuser@ds.study.iitm.ac.in",
        "password": "wrongPass@1"
    }
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid credentials"
