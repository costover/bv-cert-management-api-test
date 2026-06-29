from pathlib import Path
from pydantic import AnyHttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "BV Resources Certification Service"
    API_VERSION_STR: str = "/api/v1"
    ENVIRONMENT: str = "local"

    PORT: int = 8000
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_ECHO: bool = False

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Dynamically assembles the asynchronous PostgreSQL connection string."""
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


# Instantiate the class to make it an imported singleton across the application
settings = Settings()