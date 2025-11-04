import pytest

from app.models.tag import Tag
from app.models.user import User
from app.services.validators.integrity import (
    BaseIntegrityValidator,
    IntegrityValidatorException,
    Relation,
)


async def test_validate_single_value(db, test_user):
    integrity_validator = BaseIntegrityValidator(db=db)
    integrity_validator.relations = [
        Relation(field="user_id", model=User, is_multiple=False),
    ]

    await integrity_validator.validate(data={"user_id": test_user.id})

    with pytest.raises(IntegrityValidatorException):
        await integrity_validator.validate(data={"user_id": 999})


async def test_validate_multiple_values(db, test_tag):
    integrity_validator = BaseIntegrityValidator(db=db)
    integrity_validator.relations = [
        Relation(field="tags_ids", model=Tag, is_multiple=True),
    ]

    await integrity_validator.validate(
        data={"tags_ids": [test_tag.id]}
    )  # valid id reference
    await integrity_validator.validate(
        data={"tags_ids": []}
    )  # nothing to validtate, omit

    with pytest.raises(IntegrityValidatorException):
        await integrity_validator.validate(data={"tags_ids": [999]})

    with pytest.raises(IntegrityValidatorException):
        await integrity_validator.validate(data={"tags_ids": 999})
