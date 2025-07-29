from typing import ClassVar

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from starlette import status

from cleanstack.exceptions import AlreadyExistsError, DomainError, NotFoundError
from cleanstack.logger import logger


class ExceptionRegistry:
    _exc_mapping: ClassVar[dict[type[Exception], int]] = {
        NotFoundError: status.HTTP_404_NOT_FOUND,
        AlreadyExistsError: status.HTTP_409_CONFLICT,
    }

    @classmethod
    def register(cls, exc: type[Exception], status_code: int) -> None:
        cls._exc_mapping[exc] = status_code

    @classmethod
    def get_status_code(cls, exc: Exception) -> int | None:
        return next(
            (
                cls._exc_mapping[exc_class]
                for exc_class in type(exc).mro()
                if exc_class in cls._exc_mapping
            ),
            None,
        )


def add_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def app_exception_handler(request: Request, error: DomainError) -> Response:
        status_code = ExceptionRegistry.get_status_code(error)
        if status_code:
            return JSONResponse(
                status_code=status_code,
                content={"detail": str(error)},
            )

        logger.error("Unhandled DomainError", exc_info=True)
        return PlainTextResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )
