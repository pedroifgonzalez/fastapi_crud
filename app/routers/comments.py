from fastapi import APIRouter, Depends

from app.core.mappers.comments import CommentMapper
from app.routers.dependencies import (
    get_business_validator,
    get_comment_integrity_validator,
    get_comment_mapper,
    get_comment_service,
)
from app.schemas.comment import CommentIn, CommentOut, CommentUpdate
from app.services.comments import CommentService
from app.services.validators.business import BaseBusinessValidator
from app.services.validators.integrity import CommentIntegrityValidator

router = APIRouter()


@router.get("/", response_model=list[CommentOut])
async def get_all_comments(
    service: CommentService = Depends(get_comment_service),
    mapper: CommentMapper = Depends(get_comment_mapper),
) -> list[CommentOut]:
    return [
        mapper.to_output(db_record=db_record) for db_record in await service.find_all()
    ]


@router.get("/{id}", response_model=CommentOut)
async def get_comment(
    id: int,
    service: CommentService = Depends(get_comment_service),
    mapper: CommentMapper = Depends(get_comment_mapper),
    business_validator: BaseBusinessValidator = Depends(get_business_validator),
) -> CommentOut:
    db_record = await service.find_one(id=id)
    business_validator.check_not_deleted(db_record=db_record)
    return mapper.to_output(db_record=db_record)


@router.post("/", response_model=CommentOut)
async def create_comment(
    data: CommentIn,
    service: CommentService = Depends(get_comment_service),
    mapper: CommentMapper = Depends(get_comment_mapper),
    integrity_validator: CommentIntegrityValidator = Depends(
        get_comment_integrity_validator
    ),
) -> CommentOut:
    await integrity_validator.validate(data.model_dump())
    domain_data = await mapper.to_domain(data)
    db_record = await service.create(data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.put("/{id}", response_model=CommentOut)
async def update_comment(
    id: int,
    data: CommentUpdate,
    service: CommentService = Depends(get_comment_service),
    mapper: CommentMapper = Depends(get_comment_mapper),
    integrity_validator: CommentIntegrityValidator = Depends(
        get_comment_integrity_validator
    ),
) -> CommentOut:
    await integrity_validator.validate(data.model_dump())
    domain_data = await mapper.to_domain(data=data)
    db_record = await service.update(id=id, data=domain_data)
    return mapper.to_output(db_record=db_record)


@router.delete("/{id}")
async def delete_comment(
    id: int, service: CommentService = Depends(get_comment_service)
) -> None:
    return await service.delete(id=id)
