import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.core.database import Base


class PartyCredential(Base):
    __tablename__ = "party_credential"

    credential_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    party_id: Mapped[str] = mapped_column(ForeignKey("party.party_id"), index=True)
    course_id: Mapped[str] = mapped_column(ForeignKey("course.course_id"), index=True)
    from_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    thru_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    party: Mapped["Party"] = relationship(back_populates="credentials")
    course: Mapped["Course"] = relationship(back_populates="credentials")