import requests
from tests import ENDPOINTS

def test_signup_success(valid_user):
    """Test for successful user registration"""
    response = requests.post(ENDPOINTS["signup"], data=valid_user)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

def test_signup_password_mismatch():
    """Test registration fails when passwords do not match"""
    user_data = {
        "email": "dummyuser@mail.com",
        "password": "dummyPass@1",
        "password_confirm": "wrongPass@111",
        "fname": "Dummy",
        "lname": "User",
        "is_instructor": "false"
    }
    response = requests.post(ENDPOINTS["signup"], data=user_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Passwords do not match"

def test_signup_missing_fields():
    """Test registration fails for missing required fields"""
    user_data = {
        "email": "dummyuser@mail.com",
        "password": "dummyPass@1",
        "password_confirm": "dummyPass@1",
        "is_instructor": "false"
        # Missing 'fname' and 'lname'
    }
    response = requests.post(ENDPOINTS["signup"], data=user_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Missing required fields"

def test_signup_existing_user(valid_user):
    """Test registration fails for an existing user"""
    requests.post(ENDPOINTS["signup"], data=valid_user)
    response = requests.post(ENDPOINTS["signup"], data=valid_user)
    assert response.status_code == 400
    assert response.json()["error"] == "User already exists"

def test_login_success(valid_user):
    """Test successful user login"""
    # Ensure user is registered
    requests.post(ENDPOINTS["signup"], data=valid_user)

    login_data = {
        "email": valid_user["email"],
        "password": valid_user["password"]
    }
    response = requests.post(ENDPOINTS["login"], data=login_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"

def test_login_invalid_credentials():
    """Test login fails with incorrect credentials"""
    login_data = {
        "email": "dummyuser@mail.com",
        "password": "wrongPass@1"
    }
    response = requests.post(ENDPOINTS["login"], data=login_data)
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid credentials"

def test_logout(valid_user):
    """Test successful user logout using session cookies"""
    session = requests.Session()

    login_data = {
        "email": valid_user["email"],
        "password": valid_user["password"]
    }

    # Log in to get session cookie
    login_response = session.post(
        ENDPOINTS["login"], 
        data=login_data
    )
    
    assert login_response.status_code == 200

    # Logout request using session
    response = session.post(ENDPOINTS["logout"])
    
    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"

def test_delete_user(valid_user):
    """Test for deleting a registered user"""
    
    # Log in to get user_id
    login_data = {
        "email": valid_user["email"],
        "password": valid_user["password"]
    }
    login_response = requests.post(ENDPOINTS["login"], data=login_data)
    assert login_response.status_code == 200
    user_id = login_response.json()['user']['id']
    
    # Delete the user
    data = {"secret_key": "mysecretkey"}  # Use the actual secret key
    response = requests.delete(ENDPOINTS["user_delete"].format(user_id=user_id), data=data)

    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
