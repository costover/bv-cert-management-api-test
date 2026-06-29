from typing import AsyncGenerator, Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database import async_session_factory
from src.core.exceptions import RecordNotFoundError
from src.core.models.auth import UserLogin
from src.modules.auth.repository import AuthRepository

bearer_scheme = HTTPBearer()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields a database session instance per HTTP request.
    Automatically closes or rolls back the transaction when done.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_current_user(
    db: AsyncSession = Depends(get_db_session),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> UserLogin:
    """
    FastAPI dependency used to protect routes.
    Parses, decodes, and validates incoming JWT bearer header tokens.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode signature against global secrets config
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_login: UserLogin = await AuthRepository.get_user_login_by_id(db, user_id)
        return user_login

    except (jwt.PyJWTError, ValueError, RecordNotFoundError):
        raise credentials_exception