from fastapi.exceptions import HTTPException


class AppException(HTTPException):
    pass
