"""Tests for refresh token endpoint."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.auth import create_refresh_token, router

# Create a test app and include the router
app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestRefreshEndpoint:
    """Tests for POST /auth/refresh endpoint."""

    def test_refresh_token_returns_new_access(self, client: TestClient):
        """Test that refresh token endpoint returns a new access token."""
        refresh_token = create_refresh_token({"sub": "user@example.com", "user_id": 2})

        response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_token_with_invalid_token(self, client: TestClient):
        """Test that refresh token endpoint rejects invalid tokens."""
        response = client.post("/auth/refresh", json={"refresh_token": "invalid_token"})

        assert response.status_code == 401

    def test_refresh_token_with_access_token_fails(self, client: TestClient):
        """Test that refresh token endpoint rejects access tokens."""
        from src.api.auth import create_access_token

        access_token = create_access_token({"sub": "user@example.com", "user_id": 2})

        response = client.post("/auth/refresh", json={"refresh_token": access_token})

        assert response.status_code == 401

    def test_refresh_token_with_revoked_token_fails(self, client: TestClient):
        """Test that refresh token endpoint rejects revoked tokens."""
        from src.api.auth import REVOKED_REFRESH_TOKENS

        refresh_token = create_refresh_token({"sub": "user@example.com", "user_id": 2})

        # Revoke the token
        REVOKED_REFRESH_TOKENS.add(refresh_token)

        try:
            response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

            assert response.status_code == 401
            assert "revoked" in response.json()["detail"].lower()
        finally:
            # Cleanup: remove the token from revoked set
            REVOKED_REFRESH_TOKENS.discard(refresh_token)
