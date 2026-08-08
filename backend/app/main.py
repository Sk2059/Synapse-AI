from fastapi import FastAPI

from app.core.config import settings
from app.api.users import router as users_router
from app.api.auth import router as auth_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.include_router(
    auth_router,
    prefix="/api/v1",
)
app.include_router(
    users_router,
    prefix="/api/v1",
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "project": settings.APP_NAME,
    }