from app.api.app import create_fastapi_app
from app.core.settings import Settings

settings = Settings()  # ty:ignore[missing-argument]
app = create_fastapi_app(settings=settings)
