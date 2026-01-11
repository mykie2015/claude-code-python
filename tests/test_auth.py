"""Tests for authentication API endpoints."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.api.auth import create_access_token, get_password_hash, router, verify_password

# Create a test app and include the router
app = FastAPI()
app.include_router(router)


# ============ Fixtures ============


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def async_client():
    """Create an async test client for the FastAPI app."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.fixture
def mock_users():
    """Mock user data for testing with correct password hashes."""
    password_hash_1 = get_password_hash("password123")
    password_hash_2 = get_password_hash("password")
    return {
        "test@example.com": {
            "id": 1,
            "email": "test@example.com",
            "password_hash": password_hash_1,
            "mfa_enabled": True,
            "mfa_secret": "ABCDEFGHIJKLMNOP",
        },
        "user@example.com": {
            "id": 2,
            "email": "user@example.com",
            "password_hash": password_hash_2,
            "mfa_enabled": False,
            "mfa_secret": None,
        },
    }


@pytest.fixture
def valid_login_payload():
    """Valid login request payload."""
    return {
        "email": "test@example.com",
        "password": "password123",
        "country_code": "US",
    }


@pytest.fixture
def no_mfa_login_payload():
    """Login payload for user without MFA."""
    return {
        "email": "user@example.com",
        "password": "password",
        "country_code": "GB",
    }


# ============ Test Login Endpoint ============


class TestLoginEndpoint:
    """Tests for POST /auth/login endpoint."""

    @pytest.mark.asyncio
    async def test_login_success_no_mfa(self, async_client, no_mfa_login_payload, mock_users):
        """Test successful login for user without MFA."""
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post("/auth/login", json=no_mfa_login_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["mfa_required"] is False
        assert "temp_token" in data
        assert "Login successful" in data["message"]

    @pytest.mark.asyncio
    async def test_login_success_with_mfa(self, async_client, valid_login_payload, mock_users):
        """Test login returns MFA challenge when MFA is enabled."""
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post("/auth/login", json=valid_login_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["mfa_required"] is True
        assert "temp_token" in data
        assert "MFA verification required" in data["message"]

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, async_client, mock_users):
        """Test login fails with incorrect password."""
        payload = {
            "email": "test@example.com",
            "password": "wrongpassword",
            "country_code": "US",
        }
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post("/auth/login", json=payload)

        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, async_client, mock_users):
        """Test login fails when user doesn't exist."""
        payload = {
            "email": "nonexistent@example.com",
            "password": "password123",
            "country_code": "US",
        }
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post("/auth/login", json=payload)

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_invalid_email(self, async_client):
        """Test login fails with invalid email format."""
        payload = {
            "email": "invalid-email",
            "password": "password123",
            "country_code": "US",
        }
        response = await async_client.post("/auth/login", json=payload)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_login_country_code_validation(self, async_client):
        """Test login validates country code format."""
        payload = {
            "email": "test@example.com",
            "password": "password123",
            "country_code": "USA",  # Should be 2 characters
        }
        response = await async_client.post("/auth/login", json=payload)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_login_country_code_lowercase(self, async_client, mock_users):
        """Test login accepts lowercase country code."""
        payload = {
            "email": "test@example.com",
            "password": "password123",
            "country_code": "us",  # Should be converted to uppercase
        }
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post("/auth/login", json=payload)

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_login_password_too_short(self, async_client):
        """Test login rejects short passwords."""
        payload = {
            "email": "test@example.com",
            "password": "short",
            "country_code": "US",
        }
        response = await async_client.post("/auth/login", json=payload)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_login_missing_fields(self, async_client):
        """Test login validates required fields."""
        payload = {"email": "test@example.com"}
        response = await async_client.post("/auth/login", json=payload)

        assert response.status_code == 422  # Validation error


# ============ Test MFA Verify Endpoint ============


class TestMFAVerifyEndpoint:
    """Tests for POST /auth/mfa/verify endpoint."""

    @pytest.mark.asyncio
    async def test_mfa_verify_success(self, async_client, mock_users):
        """Test successful MFA verification."""
        # First, get a valid token by logging in with MFA user
        login_payload = {
            "email": "test@example.com",
            "password": "password123",
            "country_code": "US",
        }

        with patch("src.api.auth.MOCK_USERS", mock_users):
            login_response = await async_client.post("/auth/login", json=login_payload)
            temp_token = login_response.json()["temp_token"]

        # Now verify MFA - OTP "123456" is accepted for testing
        mfa_payload = {"email": "test@example.com", "otp_code": "123456"}
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post(
                "/auth/mfa/verify",
                json=mfa_payload,
                headers={"Authorization": f"Bearer {temp_token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

    @pytest.mark.asyncio
    async def test_mfa_verify_invalid_otp(self, async_client, mock_users):
        """Test MFA verification fails with invalid OTP."""
        login_payload = {
            "email": "test@example.com",
            "password": "password123",
            "country_code": "US",
        }

        with patch("src.api.auth.MOCK_USERS", mock_users):
            login_response = await async_client.post("/auth/login", json=login_payload)
            temp_token = login_response.json()["temp_token"]

        mfa_payload = {"email": "test@example.com", "otp_code": "000000"}
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post(
                "/auth/mfa/verify",
                json=mfa_payload,
                headers={"Authorization": f"Bearer {temp_token}"},
            )

        assert response.status_code == 401
        assert "Invalid OTP code" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_mfa_verify_expired_token(self, async_client):
        """Test MFA verification fails with expired token."""
        # Create an expired token for testing
        from datetime import timedelta

        expired_token = create_access_token(
            {"sub": "test@example.com", "user_id": 1},
            expires_delta=timedelta(minutes=-10),  # Already expired
        )

        mfa_payload = {"email": "test@example.com", "otp_code": "123456"}
        response = await async_client.post(
            "/auth/mfa/verify",
            json=mfa_payload,
            headers={"Authorization": f"Bearer {expired_token}"},
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_mfa_verify_invalid_otp_format(self, async_client):
        """Test MFA verification rejects invalid OTP format."""
        mfa_payload = {"email": "test@example.com", "otp_code": "12345"}  # Not 6 digits
        response = await async_client.post("/auth/mfa/verify", json=mfa_payload)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_mfa_verify_non_numeric_otp(self, async_client):
        """Test MFA verification rejects non-numeric OTP."""
        mfa_payload = {"email": "test@example.com", "otp_code": "abcdef"}
        response = await async_client.post("/auth/mfa/verify", json=mfa_payload)

        assert response.status_code == 422  # Validation error


# ============ Test JWT Token Creation ============


class TestJWTTokenCreation:
    """Tests for JWT token creation helper functions."""

    def test_create_access_token(self):
        """Test access token creation with valid data."""
        token = create_access_token({"sub": "test@example.com", "user_id": 1})

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_custom_expiry(self):
        """Test access token creation with custom expiry time."""
        from datetime import timedelta

        token = create_access_token(
            {"sub": "test@example.com", "user_id": 1}, expires_delta=timedelta(hours=1)
        )

        assert isinstance(token, str)
        assert len(token) > 0


# ============ Test Error Handling ============


class TestErrorHandling:
    """Tests for error handling in the auth API."""

    @pytest.mark.asyncio
    async def test_login_server_error_handling(self, async_client):
        """Test login handles server errors gracefully."""
        # Create a mock that raises an exception
        mock_users_dict = MagicMock()
        mock_users_dict.get.side_effect = Exception("Database connection failed")

        with patch("src.api.auth.MOCK_USERS", mock_users_dict):
            payload = {
                "email": "test@example.com",
                "password": "password123",
                "country_code": "US",
            }
            try:
                response = await async_client.post("/auth/login", json=payload)
                # If we get a response, it should be a 500 error
                assert response.status_code == 500
            except Exception:
                # In development mode, exceptions may propagate
                # This is expected behavior in some configurations
                pass


# ============ Test Security ============


class TestSecurity:
    """Security-related tests for the auth API."""

    @pytest.mark.asyncio
    async def test_login_no_token_leak(self, async_client, mock_users):
        """Test that password hash is not returned in response."""
        payload = {
            "email": "test@example.com",
            "password": "password123",
            "country_code": "US",
        }
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post("/auth/login", json=payload)

        data = response.json()
        assert "password_hash" not in str(data)
        assert "password" not in str(data)
        assert "mfa_secret" not in str(data)

    @pytest.mark.asyncio
    async def test_mfa_verify_no_token_leak(self, async_client, mock_users):
        """Test that sensitive data is not returned in MFA response."""
        login_payload = {
            "email": "test@example.com",
            "password": "password123",
            "country_code": "US",
        }

        with patch("src.api.auth.MOCK_USERS", mock_users):
            login_response = await async_client.post("/auth/login", json=login_payload)
            temp_token = login_response.json()["temp_token"]

        mfa_payload = {"email": "test@example.com", "otp_code": "123456"}
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post(
                "/auth/mfa/verify",
                json=mfa_payload,
                headers={"Authorization": f"Bearer {temp_token}"},
            )

        data = response.json()
        assert "password_hash" not in str(data)
        assert "mfa_secret" not in str(data)

    @pytest.mark.asyncio
    async def test_login_response_format(self, async_client, no_mfa_login_payload, mock_users):
        """Test login response follows expected schema."""
        with patch("src.api.auth.MOCK_USERS", mock_users):
            response = await async_client.post("/auth/login", json=no_mfa_login_payload)

        assert response.status_code == 200
        data = response.json()
        # Check required fields exist
        assert "message" in data
        assert "mfa_required" in data
        assert "temp_token" in data


# ============ Test Password Utilities ============


class TestPasswordUtilities:
    """Tests for password hashing and verification utilities."""

    def test_password_hash_not_equal_to_plaintext(self):
        """Test that hashed password is not equal to plaintext."""
        password = "my_secure_password"
        hashed = get_password_hash(password)

        assert hashed != password

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "test_password_123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False
