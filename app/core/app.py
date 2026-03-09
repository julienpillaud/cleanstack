from app.api.app import create_fastapi_app
from app.core.config import Settings

settings = Settings()
app = create_fastapi_app(settings=settings)
