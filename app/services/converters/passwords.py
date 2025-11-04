import bcrypt

from app.core.config import settings


class PasswordConverter:
    def __init__(self) -> None:
        self.rounds = settings.BCRYPT_ROUNDS

    def to_hash(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")
