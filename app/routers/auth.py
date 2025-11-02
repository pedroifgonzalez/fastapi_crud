from fastapi import APIRouter, Depends

from app.core.mappers.users import UserMapper
from app.routers.dependencies import get_user_mapper, get_user_service
from app.schemas.user import UserIn, UserOut
from app.services.users import UserService

router = APIRouter()


@router.post("/signup", response_model=UserOut)
async def signup(
    data: UserIn,
    mapper: UserMapper = Depends(get_user_mapper),
    service: UserService = Depends(get_user_service),
) -> UserOut:
    domain_data = await mapper.to_domain(data)
    db_record = await service.create(data=domain_data)
    return mapper.to_output(db_record=db_record)
