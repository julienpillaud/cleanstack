from fastapi import FastAPI, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.domain.exceptions import (
    BadRequestError,
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    UnprocessableContentError,
)
from cleanstack.exceptions import RepositoryError, get_status_error

ERROR_MAPPING: dict[type[DomainError], int] = {
    BadRequestError: status.HTTP_400_BAD_REQUEST,
    ForbiddenError: status.HTTP_403_FORBIDDEN,
    NotFoundError: status.HTTP_404_NOT_FOUND,
    ConflictError: status.HTTP_409_CONFLICT,
    UnprocessableContentError: status.HTTP_422_UNPROCESSABLE_CONTENT,
}


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_exception_handler(
        request: Request,
        exc: DomainError,
    ) -> JSONResponse:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        for error_cls in type(exc).mro():
            if issubclass(error_cls, DomainError) and error_cls in ERROR_MAPPING:
                status_code = ERROR_MAPPING[error_cls]
                break

        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    @app.exception_handler(RepositoryError)
    async def repository_exception_handler(
        request: Request,
        exc: RepositoryError,
    ) -> JSONResponse:
        status_code = get_status_error(exc)
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})
