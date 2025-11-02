from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import AppException
from app.core.mappers.auth import AuthMapper
from app.core.mappers.users import UserMapper
from app.core.security.tokens import TokenGenerator
from app.models.user import User
from app.routers.dependencies import (
    get_auth_mapper,
    get_business_validator,
    get_password_validator,
    get_token_generator,
    get_user_mapper,
    get_user_service,
)
from app.schemas.auth import AccessToken
from app.schemas.user import UserIn, UserOut
from app.services.users import UserService
from app.services.validators.business import BaseBusinessValidator
from app.services.validators.passwords import PasswordValidator
from app.utils.constants import WRONG_CREDENTIALS

router = APIRouter()


@router.post("/signup", response_model=UserOut)
async def signup(
    data: UserIn,
    mapper: UserMapper = Depends(get_user_mapper),
    service: UserService = Depends(get_user_service),
    business_validator: BaseBusinessValidator = Depends(get_business_validator),
) -> UserOut:
    domain_data = await mapper.to_domain(data)
    await business_validator.check_not_existent(
        model=User, field="email", value=data.email
    )
    db_record = await service.create(data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    mapper: AuthMapper = Depends(get_auth_mapper),
    service: UserService = Depends(get_user_service),
    token_generator: TokenGenerator = Depends(get_token_generator),
    password_validator: PasswordValidator = Depends(get_password_validator),
) -> AccessToken:
    domain_data = await mapper.to_domain(form_data=form_data)
    db_record = await service.find_by_email(
        email=domain_data["email"],
        raise_custom=AppException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=WRONG_CREDENTIALS,
        ),
    )
    password_validator.validate(
        password=domain_data["password"], hashed_password=db_record.hashed_password
    )
    token, token_type = token_generator.generate_access_token(
        data=domain_data["encode"]
    )
    return mapper.to_output(token=token, token_type=token_type)
