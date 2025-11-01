from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.tag import Tag
from app.models.user import User
from app.utils.constants import NOT_FOUND_ERROR


@dataclass
class Relation:
    field: str
    model: Any
    is_multiple: bool


class IntegrityValidatorException(Exception):
    pass


class BaseIntegrityValidator:
    relations: list[Relation] = []

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def validate(self, data: dict) -> dict:
        for relation in self.relations:
            field_name = relation.field
            if not data.get(field_name):
                continue
            value = data.get(field_name)

            if relation.is_multiple:
                if not isinstance(value, Iterable):
                    raise IntegrityValidatorException(
                        f"Expected iterable for field '{field_name}'"
                    )
                ids: Sequence[int] = list(value)
                if not ids:
                    continue

                stmt = select(relation.model.id).where(relation.model.id.in_(ids))
                result = await self.db.execute(stmt)
                existing_ids = set(result.scalars().all())
                missing = set(ids) - existing_ids
                if missing:
                    raise IntegrityValidatorException(
                        NOT_FOUND_ERROR.format(relation.model.__name__, missing.pop())
                    )
            else:
                stmt = select(relation.model.id).where(relation.model.id == value)
                result = await self.db.execute(stmt)
                exists = result.scalar()
                if not exists:
                    raise IntegrityValidatorException(
                        NOT_FOUND_ERROR.format(relation.model.__name__, value)
                    )

        return data


class PostIntegrityValidator(BaseIntegrityValidator):

    relations = [
        Relation(field="tags_ids", model=Tag, is_multiple=True),
        Relation(field="user_id", model=User, is_multiple=False),
    ]
