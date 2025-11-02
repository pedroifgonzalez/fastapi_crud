from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import TypedDict

from app.schemas.auth import AccessToken


class FormDataDomain(TypedDict):
    email: str
    password: str
    encode: dict


class AuthMapper:

    async def to_domain(self, form_data: OAuth2PasswordRequestForm) -> FormDataDomain:
        return FormDataDomain(
            email=form_data.username,
            password=form_data.password,
            encode={"sub": form_data.username},
        )

    def to_output(self, token: str, token_type: str) -> AccessToken:
        data = {
            "access_token": token,
            "token_type": token_type,
        }
        return AccessToken.model_validate(data)
