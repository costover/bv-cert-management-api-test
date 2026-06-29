from fastapi import APIRouter
from src.modules.auth.router import router as auth_router
from src.modules.courses.router import router as courses_router
from src.modules.parties.router import router as parties_router
from src.modules.credentials.router import router as credentials_router

# 1. Instantiate the root API router
api_router = APIRouter()

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    courses_router,
    prefix="/courses",
    tags=["Courses"]
)

api_router.include_router(
    parties_router,
    prefix="/parties",
    tags=["Parties"]
)

api_router.include_router(
    credentials_router,
    prefix="/credentials",
    tags=["Credentials"]
)