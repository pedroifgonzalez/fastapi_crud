from fastapi import APIRouter, Depends

from app.core.mappers.tags import TagMapper
from app.routers.dependencies import (
    get_business_validator,
    get_tag_mapper,
    get_tag_service,
)
from app.schemas.tag import TagIn, TagOut, TagUpdate
from app.services.tags import TagsService
from app.services.validators.business import BaseBusinessValidator

router = APIRouter()


@router.get("/", response_model=list[TagOut])
async def get_all_tags(
    service: TagsService = Depends(get_tag_service),
    mapper: TagMapper = Depends(get_tag_mapper),
) -> list[TagOut]:
    return [
        mapper.to_output(db_record=tag_record)
        for tag_record in await service.find_all()
    ]


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
) -> TagOut:
    domain_data = await mapper.to_domain(data)
    db_record = await service.create(data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.put("/{id}", response_model=TagOut)
async def update_post(
    id: int,
    data: TagUpdate,
    service: TagsService = Depends(get_tag_service),
    mapper: TagMapper = Depends(get_tag_mapper),
) -> TagOut:
    domain_data = await mapper.to_domain(data=data)
    db_record = await service.update(id=id, data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.delete("/{id}")
async def delete_tag(id: int, service: TagsService = Depends(get_tag_service)) -> None:
    return await service.delete(id=id)
