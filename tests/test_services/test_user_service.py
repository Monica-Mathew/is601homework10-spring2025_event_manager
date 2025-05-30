from builtins import range
from unittest.mock import AsyncMock, MagicMock
from pydantic import ValidationError
import pytest
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User
from app.services.user_service import UserService
from fastapi import HTTPException

pytestmark = pytest.mark.asyncio

# Test creating a user with valid data
async def test_create_user_with_valid_data(db_session, email_service,mocker):
    
    # Mock the email service to prevent sending real emails
    mock_send_email = AsyncMock()
    mocker.patch.object(email_service, 'send_verification_email', mock_send_email)
    user_data = {
        "email": "valid_user@example.com",
        "password": "ValidPassword123!",
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test creating a user with invalid data
async def test_create_user_with_invalid_data(db_session, email_service):
    user_data = {
        "nickname": "",  # Invalid nickname
        "email": "invalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is None

# Test fetching a user by ID when the user exists
async def test_get_by_id_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_id(db_session, user.id)
    assert retrieved_user.id == user.id

# Test fetching a user by ID when the user does not exist
async def test_get_by_id_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    retrieved_user = await UserService.get_by_id(db_session, non_existent_user_id)
    assert retrieved_user is None

# Test fetching a user by nickname when the user exists
async def test_get_by_nickname_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_nickname(db_session, user.nickname)
    assert retrieved_user.nickname == user.nickname

# Test fetching a user by nickname when the user does not exist
async def test_get_by_nickname_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_nickname(db_session, "non_existent_nickname")
    assert retrieved_user is None

# Test fetching a user by email when the user exists
async def test_get_by_email_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_email(db_session, user.email)
    assert retrieved_user.email == user.email

# Test fetching a user by email when the user does not exist
async def test_get_by_email_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_email(db_session, "non_existent_email@example.com")
    assert retrieved_user is None

# Test updating a user with valid data
async def test_update_user_valid_data(db_session, user):
    new_email = "updated_email@example.com"
    updated_user = await UserService.update(db_session, user.id, {"email": new_email})
    assert updated_user is not None
    assert updated_user.email == new_email

# Test updating a user with invalid data
async def test_update_user_invalid_data(db_session, user):
    with pytest.raises(HTTPException) as excinfo:
        await UserService.update(db_session, user.id, {"email": "invalidemail"})
    
    assert excinfo.value.status_code == 400
    assert "value is not a valid email address" in excinfo.value.detail

# Test deleting a user who exists
async def test_delete_user_exists(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True

# Test attempting to delete a user who does not exist
async def test_delete_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    deletion_success = await UserService.delete(db_session, non_existent_user_id)
    assert deletion_success is False

# Test listing users with pagination
async def test_list_users_with_pagination(db_session, users_with_same_role_50_users):
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    assert len(users_page_1) == 10
    assert len(users_page_2) == 10
    assert users_page_1[0].id != users_page_2[0].id

@pytest.mark.asyncio
async def test_register_user_with_valid_data(db_session, mocker):
    # Patch the method at the class level BEFORE it's used
    mocker.patch(
        "app.services.email_service.EmailService.send_verification_email",
        new_callable=AsyncMock
    )
    mock_template_manager = MagicMock()

    # Now you can safely import and create an instance
    from app.services.email_service import EmailService
    email_service = EmailService(template_manager=mock_template_manager)

    user_data = {
        "email": "register_valid_user@example.com",
        "password": "RegisterValid123!",
    }

    from app.services.user_service import UserService
    user = await UserService.register_user(db_session, user_data, email_service)

    assert user is not None
    assert user.email == user_data["email"]



# Test attempting to register a user with invalid data
async def test_register_user_with_invalid_data(db_session, email_service):
    user_data = {
        "email": "registerinvalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is None

# Test successful user login
async def test_login_user_successful(db_session, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "MySuperPassword$1234",
    }
    logged_in_user = await UserService.login_user(db_session, user_data["email"], user_data["password"])
    assert logged_in_user is not None

# Test user login with incorrect email
async def test_login_user_incorrect_email(db_session):
    user = await UserService.login_user(db_session, "nonexistentuser@noway.com", "Password123!")
    assert user is None

# Test user login with incorrect password
async def test_login_user_incorrect_password(db_session, user):
    user = await UserService.login_user(db_session, user.email, "IncorrectPassword!")
    assert user is None

# Test account lock after maximum failed login attempts
async def test_account_lock_after_failed_logins(db_session, verified_user):
    max_login_attempts = get_settings().max_login_attempts
    for _ in range(max_login_attempts):
        await UserService.login_user(db_session, verified_user.email, "wrongpassword")
    
    is_locked = await UserService.is_account_locked(db_session, verified_user.email)
    assert is_locked, "The account should be locked after the maximum number of failed login attempts."

# Test resetting a user's password
async def test_reset_password(db_session, user):
    new_password = "NewPassword123!"
    reset_success = await UserService.reset_password(db_session, user.id, new_password)
    assert reset_success is True

# Test verifying a user's email
async def test_verify_email_with_token(db_session, user):
    token = "valid_token_example"  # This should be set in your user setup if it depends on a real token
    user.verification_token = token  # Simulating setting the token in the database
    await db_session.commit()
    result = await UserService.verify_email_with_token(db_session, user.id, token)
    assert result is True

# Test unlocking a user's account
async def test_unlock_user_account(db_session, locked_user):
    unlocked = await UserService.unlock_user_account(db_session, locked_user.id)
    assert unlocked, "The account should be unlocked"
    refreshed_user = await UserService.get_by_id(db_session, locked_user.id)
    assert not refreshed_user.is_locked, "The user should no longer be locked"

@pytest.mark.asyncio
async def test_update_bio_only(db_session, user):
    updated_bio = "Updated developer bio."
    updated_user = await UserService.update(db_session, user.id, {"bio": updated_bio})
    assert updated_user is not None
    assert updated_user.bio == updated_bio

@pytest.mark.asyncio
async def test_update_profile_picture_only(db_session, user):
    new_url = "https://example.com/new_profile_pic.jpg"
    updated_user = await UserService.update(db_session, user.id, {"profile_picture_url": new_url})
    assert updated_user is not None
    assert updated_user.profile_picture_url == new_url

@pytest.mark.asyncio
async def test_update_bio_and_profile_picture(db_session, user):
    data = {
        "bio": "Multi-field update.",
        "profile_picture_url": "https://example.com/combined_update.jpg"
    }
    updated_user = await UserService.update(db_session, user.id, data)
    assert updated_user is not None
    assert updated_user.bio == data["bio"]
    assert updated_user.profile_picture_url == data["profile_picture_url"]

@pytest.mark.asyncio
async def test_update_bio_alone(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"bio": "new_bio"})
    assert updated_user is not None
    assert updated_user.bio == "new_bio"

@pytest.mark.asyncio
async def test_update_with_valid_profile_picture_url(db_session, user):
    with pytest.raises(HTTPException) as excinfo:
        await UserService.update(db_session, user.id, {"profile_picture_url": "123"})
    
    assert excinfo.value.status_code == 400
    assert "Invalid URL format" in excinfo.value.detail

        
@pytest.mark.asyncio
async def test_update_with_no_fields_fails(db_session, user):
    data = {}
    with pytest.raises(HTTPException) as excinfo:
        await UserService.update(db_session, user.id, data)

    assert excinfo.value.status_code == 400
    assert "At least one field must be provided for update" in excinfo.value.detail



@pytest.mark.asyncio
async def test_update_with_null_values(db_session, user):
    data = {
        "bio": None,
        "profile_picture_url": 'https://linkedin.com/in/johndoe'
    }
    updated_user = await UserService.update(db_session, user.id, data)
    assert updated_user is not None
    assert updated_user.bio is None
    assert updated_user.profile_picture_url is not None

@pytest.mark.asyncio
async def test_update_with_no_profile_fields(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"first_name": "UpdatedOnly"})
    assert updated_user is not None
    assert updated_user.first_name == "UpdatedOnly"
    assert updated_user.bio == user.bio
    assert updated_user.profile_picture_url == user.profile_picture_url
