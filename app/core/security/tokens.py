from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import status
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.mappers.auth import EncodeData
from app.utils.constants import WRONG_CREDENTIALS


class TokenManager:

    def __init__(self, expires_delta: timedelta) -> None:
        self.expires_delta = expires_delta
        self.token_type = "bearer"

    def generate_access_token(self, data: EncodeData) -> tuple[str, str]:
        to_encode: dict = {}
        to_encode.update(**data)
        expire = datetime.now(timezone.utc) + self.expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt, self.token_type

    def decode_access_token(self, token: str, expected_payload_type: Any) -> dict:
        credentials_exception = AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=WRONG_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            assert expected_payload_type(**payload)
        except InvalidTokenError:
            raise credentials_exception
        except Exception:
            raise credentials_exception
        return payload
