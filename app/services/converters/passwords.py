import bcrypt


class PasswordConverter:
    def __init__(self) -> None:
        self.rounds = 10

    def to_hash(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")
