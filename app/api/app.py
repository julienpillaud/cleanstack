from fastapi import FastAPI

from app.api.containers.router import router as containers_router
from app.api.items.router import router as items_router
from app.api.lifespan import lifespan_factory
from app.core.settings import Settings
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
        lifespan=lifespan_factory(settings=settings),
    )

    add_exception_handler(app=app)
    app.include_router(items_router)
    app.include_router(containers_router)
    return app
