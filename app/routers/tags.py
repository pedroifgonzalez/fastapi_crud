from fastapi import APIRouter, Depends

from app.core.mappers.tags import TagMapper
from app.core.security.roles import UserRole
from app.models.user import User
from app.routers.dependencies import (
    get_business_validator,
    get_tag_mapper,
    get_tag_service,
)
from app.routers.dependencies.auth import require_roles
from app.schemas.tag import TagIn, TagOut, TagUpdate
from app.services.tags import TagsService
from app.services.validators.business import BaseBusinessValidator
from app.utils.pagination import PaginatedResponse, PaginationParams

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[TagOut])
async def get_all_tags(
    service: TagsService = Depends(get_tag_service),
    mapper: TagMapper = Depends(get_tag_mapper),
    pagination: PaginationParams = Depends(),
) -> PaginatedResponse[TagOut]:
    db_records, total = await service.find_all()
    items = [mapper.to_output(db_record) for db_record in db_records]
    return PaginatedResponse.create(
        items=items, total=total, page=pagination.page, page_size=pagination.page_size
    )


@router.get("/{id}", response_model=TagOut)
async def get_tag(
    id: int,
    service: TagsService = Depends(get_tag_service),
    mapper: TagMapper = Depends(get_tag_mapper),
    business_validator: BaseBusinessValidator = Depends(get_business_validator),
) -> TagOut:
    db_record = await service.find_one(id=id)
    business_validator.check_not_deleted(db_record=db_record)
    return mapper.to_output(db_record=db_record)


@router.post("/", response_model=TagOut)
async def create_tag(
    data: TagIn,
    service: TagsService = Depends(get_tag_service),
    mapper: TagMapper = Depends(get_tag_mapper),
    _: User = require_roles([UserRole.REGULAR]),
) -> TagOut:
    domain_data = await mapper.to_domain(data)
    db_record = await service.create(data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.put("/{id}", response_model=TagOut)
async def update_tag(
    id: int,
    data: TagUpdate,
    service: TagsService = Depends(get_tag_service),
    mapper: TagMapper = Depends(get_tag_mapper),
    _: User = require_roles([UserRole.REGULAR]),
) -> TagOut:
    domain_data = await mapper.to_domain(data=data)
    db_record = await service.update(id=id, data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.delete("/{id}")
async def delete_tag(
    id: int,
    service: TagsService = Depends(get_tag_service),
    _: User = require_roles([UserRole.REGULAR]),
) -> None:
    return await service.delete(id=id)
