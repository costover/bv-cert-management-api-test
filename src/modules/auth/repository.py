from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import RecordNotFoundError
from src.core.models.auth import UserLogin


class AuthRepository:
    @staticmethod
    async def get_user_login_by_id(
        db: AsyncSession,
        user_login_id: str
    ) -> UserLogin:
        user_login: UserLogin = await db.scalar(select(UserLogin).where(UserLogin.user_login_id == user_login_id))
        if not user_login:
            raise RecordNotFoundError("User not found")

        return user_login