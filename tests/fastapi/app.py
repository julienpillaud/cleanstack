from fastapi import FastAPI
from starlette import status

from cleanstack.exceptions import DomainError, NotFoundError
from cleanstack.fastapi.exceptions import ExceptionRegistry, add_exception_handler


class CustomError(DomainError):
    pass


class UnexpectedDomainError(DomainError):
    pass


app = FastAPI()


@app.get("/not-found-error")
def simulate_not_found_error() -> None:
    raise NotFoundError("Not Found")


@app.get("/custom-error")
def simulate_custom_error() -> None:
    raise CustomError("Custom Error")


@app.get("/unexpected-domain-error")
def simulate_unexpected_domain_error() -> None:
    raise UnexpectedDomainError("Unexpected Domain Error")


ExceptionRegistry.register(CustomError, status.HTTP_418_IM_A_TEAPOT)
add_exception_handler(app)
