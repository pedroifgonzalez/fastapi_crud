from fastapi import APIRouter, Depends

from app.core.mappers.users import UserMapper
from app.core.security.roles import UserRole
from app.models.user import User
from app.routers.dependencies.auth import require_roles
from app.routers.dependencies.mappers import get_user_mapper
from app.routers.dependencies.services import get_user_service
from app.schemas.user import UserIn, UserOut, UserUpdate
from app.services.users import UserService
from app.utils.pagination import PaginatedResponse, PaginationParams

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[UserOut])
async def get_all_users(
    service: UserService = Depends(get_user_service),
    mapper: UserMapper = Depends(get_user_mapper),
    pagination: PaginationParams = Depends(),
    _: User = require_roles([UserRole.ADMIN]),
) -> PaginatedResponse[UserOut]:
    db_records, total = await service.find_all(include_deleted=True)
    items = [mapper.to_output(db_record) for db_record in db_records]
    return PaginatedResponse.create(
        items=items, total=total, page=pagination.page, page_size=pagination.page_size
    )


@router.get("/{id}", response_model=UserOut)
async def get_user(
    id: int,
    service: UserService = Depends(get_user_service),
    mapper: UserMapper = Depends(get_user_mapper),
    _: User = require_roles([UserRole.ADMIN]),
) -> UserOut:
    db_record = await service.find_one(id=id, include_deleted=True)
    return mapper.to_output(db_record=db_record)


@router.post("/", response_model=UserOut)
async def create_user(
    data: UserIn,
    service: UserService = Depends(get_user_service),
    mapper: UserMapper = Depends(get_user_mapper),
    _: User = require_roles([UserRole.ADMIN]),
) -> UserOut:
    domain_data = await mapper.to_domain(data=data)
    db_record = await service.create(data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.put("/{id}", response_model=UserOut)
async def update_user(
    id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
    mapper: UserMapper = Depends(get_user_mapper),
    _: User = require_roles([UserRole.ADMIN]),
) -> UserOut:
    domain_data = await mapper.to_domain(data=data)
    db_record = await service.update(id=id, data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.delete("/{id}")
async def delete_user(
    id: int,
    service: UserService = Depends(get_user_service),
    _: User = require_roles([UserRole.ADMIN]),
) -> None:
    return await service.delete(id=id)
