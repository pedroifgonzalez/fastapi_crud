import bcrypt
from fastapi import status

from app.services.base import ServiceException
from app.utils.constants import WRONG_CREDENTIALS


class PasswordValidator:

    def validate(self, password: str, hashed_password: str) -> bool:
        password_bytes = password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        if not bcrypt.checkpw(password_bytes, hashed_bytes):
            raise ServiceException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=WRONG_CREDENTIALS,
            )
        return True
