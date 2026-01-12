def test_settings_loads_from_env():
    from src.config import Settings

    settings = Settings()
    assert settings.SECRET_KEY == "your-super-secret-key-min-32-chars-here"
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert settings.REFRESH_TOKEN_EXPIRE_DAYS == 7
    assert settings.MFA_TOKEN_EXPIRE_MINUTES == 5
