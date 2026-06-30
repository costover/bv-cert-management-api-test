from fastapi import status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import RecordNotFoundError
from src.core.models.auth import UserLogin
from src.core.security import create_access_token, hash_password, verify_password
from src.modules.auth.repository import AuthRepository
from src.modules.auth.schemas import LoginRequest, TokenResponse, UserLoginCreate


class AuthService:
    @staticmethod
    async def login(
        db: AsyncSession,
        request: LoginRequest
    ) -> TokenResponse:
        try:
            db_user_login: UserLogin = await AuthRepository.get_user_login_by_id(db, request.username)

            if not verify_password(request.password, db_user_login.password_hash):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

            token = create_access_token(request.username)

            return TokenResponse(
                access_token=token,
            )

        except RecordNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    @staticmethod
    async def get_user_login_by_id(
        db: AsyncSession,
        user_login_id: str
    ) -> UserLogin:
        try:
            user_login: UserLogin = await AuthRepository.get_user_login_by_id(db, user_login_id)
            return user_login
        except RecordNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    @staticmethod
    async def create_user_login(
        db: AsyncSession,
        user_login_in: UserLoginCreate
    ) -> UserLogin:
        existing_user = await db.scalar(select(UserLogin).where(UserLogin.user_login_id == user_login_in.user_login_id))
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this ID already exists")
        db_user = UserLogin(
            user_login_id=user_login_in.user_login_id,
            password_hash=hash_password(user_login_in.password),
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
