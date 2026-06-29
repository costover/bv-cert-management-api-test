from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserLoginResponse(BaseModel):
    user_login_id: str
    password_hash: str


class UserLoginCreate(BaseModel):
    user_login_id: str
    password: str