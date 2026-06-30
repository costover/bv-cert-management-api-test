from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user, get_db_session
from src.modules.auth.schemas import TokenResponse, LoginRequest, UserLoginResponse, UserLoginCreate
from src.modules.auth.service import AuthService

router = APIRouter()

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db_session)
) -> TokenResponse:
    return await AuthService.login(db, request)


@router.post("/user", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
async def create_user_login(
    user_login_in: UserLoginCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user)
):
    return await AuthService.create_user_login(db, user_login_in)