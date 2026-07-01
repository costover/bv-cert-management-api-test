from pydantic import BaseModel

from src.core.schema import ApiModel


class LoginRequest(ApiModel):
    username: str
    password: str


class TokenResponse(ApiModel):
    access_token: str
    token_type: str = "bearer"


class UserLoginResponse(ApiModel):
    user_login_id: str
    password_hash: str


class UserLoginCreate(ApiModel):
    user_login_id: str
    password: str