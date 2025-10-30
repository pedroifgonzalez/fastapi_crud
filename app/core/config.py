from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from env variables"""

    DATABASE_URL: str


settings = Settings()  # type: ignore
