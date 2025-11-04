from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.mappers.auth import EncodeData
from app.core.security.tokens import TokenManager
from app.models.user import User
from app.routers.dependencies.security import get_token_manager
from app.routers.dependencies.services import get_user_service
from app.services.users import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserService = Depends(get_user_service),
    token_manager: TokenManager = Depends(get_token_manager),
) -> User:
    data = token_manager.decode_access_token(
        token=token, expected_payload_type=EncodeData
    )
    db_record = await user_service.find_by_email(data["sub"])
    return db_record
