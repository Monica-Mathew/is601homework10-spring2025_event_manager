import asyncio
from builtins import str
from unittest.mock import patch
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token  # Import your FastAPI app
import pytest
from app.services.jwt_service import decode_token
from urllib.parse import urlencode

# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Define user data for the test
    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    # Send a POST request to create a user
    response = await async_client.post("/users/", json=user_data, headers=headers)
    # Asserts
    assert response.status_code == 403

# You can similarly refactor other test functions to use the async_client fixture
@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{verified_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]

@pytest.mark.asyncio
async def test_create_user_invalid_password(async_client):
    # Invalid password (too short and missing complexity)
    user_data = {
        "email": "valid@example.com",
        "password": "short",  # Invalid password (no uppercase, no special characters, too short)
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422  # Expecting validation error
    assert "detail" in response.json()
    assert "Password must be at least 8 characters long" in response.json()["detail"][0]["msg"]

@pytest.mark.asyncio
@patch("app.services.email_service.EmailService.send_verification_email")
async def test_create_user_valid_password(mock_send_email, async_client):
    # Mock the send email function to prevent real SMTP call
    mock_send_email.return_value = None

    user_data = {
        "email": "valid@example.com",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)

    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_delete_user(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{admin_user.id}", headers=headers)
    assert delete_response.status_code == 204
    # Verify the user is deleted
    fetch_response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "AnotherPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Email already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_register_invalid_email_format(async_client):
    user_data = {
        "email": "not-an-email",
        "password": "Secure*1234"
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422
    errors = response.json().get("detail", [])
    assert any("Invalid email format" in err["msg"] for err in errors)


@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

valid_emails = [
    "user@example.com",
    "user.name@example.co.uk",
    "user_name+123@example.io",
    "user-name@example-domain.com",
    "USER@EXAMPLE.COM", 
    "user123@sub.example.com" 
]


@pytest.mark.asyncio
@pytest.mark.parametrize("email", valid_emails)
@patch("app.services.email_service.EmailService.send_verification_email")
async def test_register_valid_emails(mock_send_email, async_client, email):
    mock_send_email.return_value = None  # Prevent real SMTP call

    user_data = {
        "email": email,
        "password": "StrongPass123!"  
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 200, f"Failed for email: {email}"
    response_data = response.json()
    assert "email" in response_data
    assert response_data["email"] == email.lower().strip()

invalid_emails = [
    "plainaddress",               # No @
    "@no-local-part.com",        # No local part (before the @)
    "user@.com",                 # No domain name after @
    "user@com",                  # No dot in domain
    "user@com.",                 # Ends with dot in domain
    "user@@example.com",         # Double @
    "user example@example.com",  # Space in email
    "user@example..com",         # Double dot in domain part
    "user@example.com (Joe)",    # Email with spaces and other characters
    "",                          # Empty email string
    "   ",                       # Just spaces
    "user@-example.com",         # Invalid domain starts with a hyphen
    "user@sub.-example.com"      # Invalid domain with a hyphen in the middle
]

@pytest.mark.asyncio
@pytest.mark.parametrize("email", invalid_emails)
async def test_register_invalid_emails(async_client, email):
    user_data = {
        "email": email,
        "password": "SecurePass123!"  # Assumed valid password for testing
    }

    response = await async_client.post("/register/", json=user_data)
    
    assert response.status_code == 422, f"Failed for email: {email}"
    response_data = response.json()
    assert "detail" in response_data  # Error details should be in 'detail'
    assert any("Invalid email format" in err["msg"] for err in response_data["detail"])



@pytest.mark.asyncio
async def test_login_success(async_client, verified_user):
    # Attempt to login with the test user
    form_data = {
        "username": verified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    # Check for successful login response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Use the decode_token method from jwt_service to decode the JWT
    decoded_token = decode_token(data["access_token"])
    assert decoded_token is not None, "Failed to decode token"
    assert decoded_token["role"] == "AUTHENTICATED", "The user role should be AUTHENTICATED"

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {
        "username": "nonexistentuser@here.edu",
        "password": "DoesNotMatter123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {
        "username": verified_user.email,
        "password": "IncorrectPassword123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio 
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {
        "username": unverified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    form_data = {
        "username": locked_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked due to too many failed login attempts." in response.json().get("detail", "")
@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"  # Valid UUID format
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]

@pytest.mark.asyncio
async def test_update_user_linkedin(async_client, admin_user, admin_token):
    updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert 'items' in response.json()

@pytest.mark.asyncio
async def test_list_users_as_manager(async_client, manager_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client, user_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden, as expected for regular user
