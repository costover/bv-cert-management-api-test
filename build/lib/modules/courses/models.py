import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import mapped_column, Mapped

from src.core.database import Base


class Course(Base):
    __tablename__ = "course"

    __table_args__ = {"schema": "cert_db"}

    course_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    course_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    status_id: Mapped[str] = mapped_column(String(20))
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    deadline_type_id: Mapped[Optional[str]] = mapped_column(String(20))
    deadline_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    deadline_relative: Mapped[Optional[int]] = mapped_column(Integer)
    deadline_relative_uom_id: Mapped[Optional[str]] = mapped_column(String(20))
    eleap_course_id: Mapped[Optional[str]] = mapped_column(String(255))