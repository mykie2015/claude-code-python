"""Tests for logout endpoint."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.auth import create_refresh_token, router


# Create a test app and include the router
app = FastAPI()
app.include_router(router)


def test_logout_revokes_refresh_token():
    """Test that logout successfully revokes a refresh token."""
    # Create a refresh token
    refresh_token = create_refresh_token({"sub": "user@example.com", "user_id": 2})

    client = TestClient(app)
    response = client.post("/auth/logout", json={"refresh_token": refresh_token})

    assert response.status_code == 200

    # Token should now be invalid
    response2 = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response2.status_code == 401
