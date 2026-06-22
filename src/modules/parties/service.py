import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.parties.models import Party
from src.modules.parties.schemas import PartyCreate, PartyUpdate


class PartyService:
    @staticmethod
    async def create_party(
        db: AsyncSession,
        party_in: PartyCreate
    ) -> Party:
        existing_party = await db.scalar(select(Party).where(Party.eleap_user_id == party_in.eleap_user_id))
        if existing_party:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Party already exists with provided eLeap ID.")
        db_party = Party(**party_in.model_dump())
        db.add(db_party)
        await db.commit()
        await db.refresh(db_party)
        return db_party


    @staticmethod
    async def update_party(
        db: AsyncSession,
        party_id: uuid.UUID,
        party_in: PartyUpdate
    ) -> Party:
        db_party: Party = await PartyService.get_party(db, party_id)

        update_data: PartyUpdate = party_in.model_dump(exclude_unset=True)

        if "eleap_user_id" in update_data and update_data["eleap_user_id"] != db_party.eleap_user_id:
            existing_party = await db.scalar(
                select(Party).where(Party.eleap_user_id == update_data["eleap_user_id"])
            )
            if existing_party:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Party already exists with provided eLeap ID.")

        for field, value in update_data.items():
            setattr(db_party, field, value)

        db.add(db_party)
        await db.commit()
        await db.refresh(db_party)

        return db_party


    @staticmethod
    async def get_party(
        db: AsyncSession,
        party_id: uuid.UUID
    ) -> Party:
        party = await db.scalar(select(Party).where(Party.party_id == party_id))
        if not party:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party not found")
        return party