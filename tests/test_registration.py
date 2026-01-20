"""Tests for user registration endpoint."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.api.auth import router

# Create a test app and include the router
app = FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def async_client():
    """Create an async test client for the FastAPI app."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


def test_registration_success(client):
    """Test successful user registration."""
    response = client.post(
        "/auth/register",
        json={"email": "newuser@example.com", "password": "securepass123", "country_code": "US"},
    )
    assert response.status_code == 201
    assert "id" in response.json()


def test_registration_duplicate_email(client):
    """Test registration with duplicate email fails."""
    # First registration
    client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "securepass123", "country_code": "US"},
    )
    # Duplicate registration
    response = client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "anotherpass456", "country_code": "GB"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
