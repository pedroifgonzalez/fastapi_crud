from app.models.user import User
from app.schemas.user import UserIn, UserOut
from app.services.converters.passwords import PasswordConverter


class UserMapper:

    def __init__(self, password_converter: PasswordConverter) -> None:
        self.password_converter = password_converter

    async def to_domain(self, data: UserIn) -> dict:
        domain_data = data.model_dump(exclude_none=True)
        domain_data.update(
            {
                "hashed_password": self.password_converter.to_hash(
                    password=domain_data.pop("password")
                )
            }
        )
        return domain_data

    def to_output(self, db_record: User) -> UserOut:
        data = {
            "id": db_record.id,
            "name": db_record.name,
            "email": db_record.email,
            "posts": db_record.posts,
            "comments": db_record.comments,
        }
        return UserOut.model_validate(data)
