from fastapi import status
from starlette.testclient import TestClient


def test_exception_handler_existing_error(client: TestClient) -> None:
    response = client.get("/not-found-error")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}


def test_exception_handler_registered_error(client: TestClient) -> None:
    response = client.get("/custom-error")
    assert response.status_code == status.HTTP_418_IM_A_TEAPOT
    assert response.json() == {"detail": "Custom Error"}


def test_exception_handler_unhandled_error(client: TestClient) -> None:
    response = client.get("/unexpected-domain-error")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.text == "Internal Server Error"
