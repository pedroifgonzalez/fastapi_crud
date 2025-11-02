from datetime import timedelta

from app.core.config import settings
from app.core.security.tokens import TokenGenerator


def get_token_generator() -> TokenGenerator:
    return TokenGenerator(
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
