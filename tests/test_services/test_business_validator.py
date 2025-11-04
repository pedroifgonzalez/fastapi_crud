import pytest

from app.models.user import User
from app.services.validators.business import BaseBusinessValidator, BusinessException


def test_check_not_deleted(db, test_tag, test_deleted_tag):
    business_validator = BaseBusinessValidator(db)

    # does not raise any error
    business_validator.check_not_deleted(test_tag)

    # raises an error
    with pytest.raises(BusinessException):
        business_validator.check_not_deleted(test_deleted_tag)


async def test_check_not_existent(db, test_user):
    business_validator = BaseBusinessValidator(db)

    # does not raise any error
    await business_validator.check_not_existent(
        model=User, field="email", value="nonexistentemail@gmail.com"
    )

    # raises an error
    with pytest.raises(BusinessException):
        await business_validator.check_not_existent(
            model=User, field="email", value=test_user.email
        )
