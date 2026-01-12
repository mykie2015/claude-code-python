from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = "your-super-secret-key-min-32-chars-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MFA_TOKEN_EXPIRE_MINUTES: int = 5

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
