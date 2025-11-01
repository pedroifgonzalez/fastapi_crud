from typing import Generic, TypeVar

from app.core.exceptions import AppException
from app.models.base import Base
from app.utils.constants import NOT_FOUND_ERROR

T = TypeVar("T", bound=Base)


class BusinessException(AppException):
    pass


class BaseBusinessValidator(Generic[T]):

    def check_not_deleted(self, db_record: T) -> None:
        if db_record.is_deleted:  # type: ignore
            raise BusinessException(
                status_code=404,
                detail=NOT_FOUND_ERROR.format(
                    db_record.__class__.__name__, db_record.id  # type: ignore
                ),
            )
