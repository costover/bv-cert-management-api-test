from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings

# 1. Initialize password hashing context (Uses bcrypt with 12 work factor rounds by default)
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Set up the token extraction scheme for endpoints
# This matches the route path in src/modules/auth/router.py where users exchange credentials
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_VERSION_STR}/auth/login")


# --- HASHING UTILITIES ---

def hash_password(password: str) -> str:
    """Generates a secure cryptographic hash from a plain text password."""
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashed_password_str = hashed_password_bytes.decode('utf-8')
    return hashed_password_str
    


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that an incoming password matches the existing stored hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


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
