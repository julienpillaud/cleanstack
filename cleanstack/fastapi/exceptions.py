import traceback
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
    async def app_exception_handler(request: Request, exc: DomainError) -> Response:
        status_code = ExceptionRegistry.get_status_code(exc)
        if status_code:
            return JSONResponse(
                status_code=status_code,
                content={"detail": str(exc)},
            )

        logger.error(f"Unhandled DomainError\n{unhandled_error_log(exc)}")
        return PlainTextResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )


def unhandled_error_log(exc: BaseException) -> str:
    location = extract_exception_location(exc)
    message = "Consider to register with 'ExceptionRegistry.register'"
    return f"{location}\n    raise {exc!r}\n{message}"


def extract_exception_location(exc: BaseException) -> str:
    tb = exc.__traceback__
    if not tb:
        return "Unknown location"

    while tb.tb_next:
        tb = tb.tb_next

    summary = traceback.extract_tb(tb)
    frame = summary[-1]
    return f'File "{frame.filename}", line {frame.lineno}, in {frame.name}'
