from app.api.app import create_fastapi_app
from app.core.config import Settings
from app.core.init import initialize_app

settings = Settings()
app = create_fastapi_app(settings=settings)
initialize_app(settings=settings)
