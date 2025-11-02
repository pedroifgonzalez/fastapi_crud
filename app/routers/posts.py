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

router = APIRouter()


@router.get("/", response_model=list[PostOut])
async def get_all_posts(
    service: PostService = Depends(get_post_service),
    mapper: PostMapper = Depends(get_post_mapper),
) -> list[PostOut]:
    return [
        mapper.to_output(db_record=db_record) for db_record in await service.find_all()
    ]


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
    _: User = Depends(get_current_user),
) -> PostOut:
    await integrity_validator.validate(data.model_dump())
    domain_data = await mapper.to_domain(data=data)
    db_record = await service.update(id=id, data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.delete("/{id}")
async def delete_post(
    id: int,
    service: PostService = Depends(get_post_service),
    _: User = Depends(get_current_user),
) -> None:
    return await service.delete(id=id)
