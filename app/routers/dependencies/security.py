from datetime import timedelta

from app.core.config import settings
from app.core.security.tokens import TokenManager


def get_token_manager() -> TokenManager:
    return TokenManager(
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
