from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.core.database import Base


class StatusItem(Base):
    __tablename__ = 'status_item'

    status_id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String(255))
    created_stamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_updated_stamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    courses: Mapped[List["Course"]] = relationship(back_populates="status")
    parties: Mapped[List["Party"]] = relationship(back_populates="status")


class Enumeration(Base):
    __tablename__ = 'enumeration'

    enum_id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    enum_type_id: Mapped[Optional[str]] = mapped_column(ForeignKey("enumeration_type.enum_type_id"))
    enum_code: Mapped[Optional[str]] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(String(255))
    created_stamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_updated_stamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    enumeration_type: Mapped["EnumerationType"] = relationship(back_populates="enumerations")
    courses: Mapped[List["Course"]] = relationship(back_populates="deadline_type")


class EnumerationType(Base):
    __tablename__ = 'enumeration_type'

    enum_type_id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String(255))
    created_stamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_updated_stamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    enumerations: Mapped[List["Enumeration"]] = relationship(back_populates="enumeration_type")