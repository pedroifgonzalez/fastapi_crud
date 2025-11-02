from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


class TokenGenerator:

    def __init__(self, expires_delta: timedelta) -> None:
        self.expires_delta = expires_delta
        self.token_type = "bearer"

    def generate_access_token(self, data: dict) -> tuple[str, str]:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + self.expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt, self.token_type
