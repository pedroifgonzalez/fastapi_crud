from fastapi import APIRouter, Depends

from app.core.mappers.posts import PostMapper
from app.routers.dependencies import (
    get_post_integrity_validator,
    get_post_mapper,
    get_post_service,
)
from app.schemas.post import PostIn, PostOut
from app.services.posts import PostService
from app.services.validators.integrity import PostIntegrityValidator

router = APIRouter()


@router.get("/", response_model=list[PostOut])
async def get_all_posts(
    service: PostService = Depends(get_post_service),
) -> list[PostOut]:
    return [
        PostOut.model_validate(post, from_attributes=True)
        for post in await service.find_all()
    ]


@router.get("/{id}", response_model=PostOut)
async def get_post(
    id: int, service: PostService = Depends(get_post_service)
) -> PostOut:
    db_record = await service.find_one(id=id)
    return PostOut.model_validate(db_record, from_attributes=True)


@router.post("/", response_model=PostOut)
async def create_post(
    data: PostIn,
    service: PostService = Depends(get_post_service),
    mapper: PostMapper = Depends(get_post_mapper),
    integrity_validator: PostIntegrityValidator = Depends(get_post_integrity_validator),
) -> PostOut:
    await integrity_validator.validate(data.model_dump())
    domain_data = mapper.to_domain(data)
    db_record = await service.create(data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.put("/{id}", response_model=PostOut)
async def update_post(
    id: int, data: PostIn, service: PostService = Depends(get_post_service)
) -> PostOut:
    db_record = await service.update(id=id, data=data.model_dump())
    return PostOut.model_validate(db_record, from_attributes=True)


@router.delete("/{id}")
async def delete_post(
    id: int, service: PostService = Depends(get_post_service)
) -> None:
    return await service.delete(id=id)
