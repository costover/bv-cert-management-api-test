import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.core.database import Base

class Course(Base):
    __tablename__ = "course"

    course_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    course_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    status_id: Mapped[str] = mapped_column(ForeignKey("status_item.status_id"))
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    deadline_type_enum_id: Mapped[Optional[str]] = mapped_column(ForeignKey("enumeration.enum_id"))
    deadline_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    deadline_relative: Mapped[Optional[int]] = mapped_column(Integer)
    deadline_relative_uom_id: Mapped[Optional[str]] = mapped_column(String(20))
    eleap_course_id: Mapped[Optional[str]] = mapped_column(String(255))

    status: Mapped["StatusItem"] = relationship(back_populates="courses")
    deadline_type: Mapped["Enumeration"] = relationship(back_populates="courses")