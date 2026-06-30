from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class UserLogin(Base):
    __tablename__ = "user_login"

    user_login_id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))