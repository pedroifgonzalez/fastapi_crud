from typing import Annotated, List

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import AppException
from app.core.mappers.auth import EncodeData
from app.core.security.roles import UserRole
from app.core.security.tokens import TokenManager
from app.models.user import User
from app.routers.dependencies.security import get_token_manager
from app.routers.dependencies.services import get_user_service
from app.services.users import UserService
from app.utils.constants import INSUFFICIENT_PERMISSIONS

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


def require_roles(allowed_roles: List[UserRole]) -> User:
    async def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in [role.value for role in allowed_roles]:
            raise AppException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=INSUFFICIENT_PERMISSIONS,
            )
        return current_user

    return Depends(dependency)
