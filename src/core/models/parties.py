import uuid
from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.core.database import Base


class Party(Base):
    __tablename__ = "party"

    party_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    party_type_id: Mapped[str] = mapped_column(ForeignKey("party_type.party_type_id"))
    status_id: Mapped[str] = mapped_column(ForeignKey("status_item.status_id"))
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    email_address: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    eleap_user_id: Mapped[Optional[str]] = mapped_column(String(255))

    status: Mapped["StatusItem"] = relationship(back_populates="parties")
    party_type: Mapped["PartyType"] = relationship(back_populates="parties")


class PartyType(Base):
    __tablename__ = "party_type"

    party_type_id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    parties: Mapped[List["Party"]] = relationship(back_populates="party_type")