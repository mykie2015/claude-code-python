"""Tests for auth config usage."""

from src.api.auth import SECRET_KEY, ALGORITHM


def test_uses_settings_config():
    """Should NOT have hardcoded SECRET_KEY."""
    assert SECRET_KEY != "your-secret-key-change-in-production"
