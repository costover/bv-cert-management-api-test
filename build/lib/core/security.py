from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings

# 1. Initialize password hashing context (Uses bcrypt with 12 work factor rounds by default)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Set up the token extraction scheme for endpoints
# This matches the route path in src/modules/auth/router.py where users exchange credentials
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_VERSION_STR}/auth/login")


# --- HASHING UTILITIES ---

def hash_password(password: str) -> str:
    """Generates a secure cryptographic hash from a plain text password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that an incoming password matches the existing stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT UTILITIES ---

def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """
    Signs and packages data into a secure, time-restricted JWT access token.
    'subject' is usually the unique User ID string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Pack claims payload (sub = Subject, exp = Expiration Time)
    to_encode = {"exp": expire, "sub": str(subject)}

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# --- AUTH DEPENDENCY ---

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
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
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return int(user_id)

    except (jwt.PyJWTError, ValueError):
        raise credentials_exception