from fastapi import FastAPI

from app.api.items.router import router as items_router
from app.core.config import Settings
from cleanstack.fastapi.exceptions import add_exception_handler


def create_fastapi_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version=settings.api_version,
        swagger_ui_parameters={
            "tryItOutEnabled": True,
            "displayRequestDuration": True,
            "persistAuthorization": True,
        },
    )

    add_exception_handler(app=app)
    app.include_router(items_router)
    return app
