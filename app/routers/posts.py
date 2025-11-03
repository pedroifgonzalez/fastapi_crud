from fastapi import APIRouter, Depends

from app.core.mappers.posts import PostMapper
from app.models.user import User
from app.routers.dependencies import (
    get_business_validator,
    get_current_user,
    get_post_integrity_validator,
    get_post_mapper,
    get_post_service,
)
from app.schemas.post import PostIn, PostOut, PostUpdate
from app.services.posts import PostService
from app.services.validators.business import BaseBusinessValidator
from app.services.validators.integrity import PostIntegrityValidator
from app.utils.pagination import PaginatedResponse, PaginationParams

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[PostOut])
async def get_all_posts(
    service: PostService = Depends(get_post_service),
    mapper: PostMapper = Depends(get_post_mapper),
    pagination: PaginationParams = Depends(),
) -> PaginatedResponse[PostOut]:
    db_records, total = await service.find_all()
    items = [mapper.to_output(db_record) for db_record in db_records]
    return PaginatedResponse.create(
        items=items, total=total, page=pagination.page, page_size=pagination.page_size
    )


@router.get("/{id}", response_model=PostOut)
async def get_post(
    id: int,
    service: PostService = Depends(get_post_service),
    mapper: PostMapper = Depends(get_post_mapper),
    business_validator: BaseBusinessValidator = Depends(get_business_validator),
) -> PostOut:
    db_record = await service.find_one(id=id)
    business_validator.check_not_deleted(db_record=db_record)
    return mapper.to_output(db_record=db_record)


@router.post("/", response_model=PostOut)
async def create_post(
    data: PostIn,
    service: PostService = Depends(get_post_service),
    mapper: PostMapper = Depends(get_post_mapper),
    integrity_validator: PostIntegrityValidator = Depends(get_post_integrity_validator),
    _: User = Depends(get_current_user),
) -> PostOut:
    await integrity_validator.validate(data.model_dump())
    domain_data = await mapper.to_domain(data)
    db_record = await service.create(data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.put("/{id}", response_model=PostOut)
async def update_post(
    id: int,
    data: PostUpdate,
    service: PostService = Depends(get_post_service),
    mapper: PostMapper = Depends(get_post_mapper),
    integrity_validator: PostIntegrityValidator = Depends(get_post_integrity_validator),
    user: User = Depends(get_current_user),
) -> PostOut:
    await integrity_validator.validate(data.model_dump())
    domain_data = await mapper.to_domain(data=data)
    db_record = await service.update_for_user(id=id, user_id=user.id, data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.delete("/{id}")
async def delete_post(
    id: int,
    service: PostService = Depends(get_post_service),
    user: User = Depends(get_current_user),
) -> None:
    return await service.delete_for_user(id=id, user_id=user.id)
