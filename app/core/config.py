import sys

from loguru import logger
from pydantic_settings import BaseSettings

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<level>{level}</level>:     <level>{message}</level>",
    enqueue=True,
    backtrace=False,
    diagnose=False,
)


class Settings(BaseSettings):
    """Application settings loaded from env variables"""

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    BCRYPT_ROUNDS: int = 10


settings = Settings()  # type: ignore
