import uuid
from typing import Any, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from src.core.models.credentials import PartyCredential
from src.modules.credentials.schemas import PartyCredentialCreate, PartyCredentialUpdate


class CredentialService:
    @staticmethod
    async def _get_party_credentials_filtered(
        db: AsyncSession,
        filters: dict[InstrumentedAttribute, Any],
    ) -> List[PartyCredential]:

        stmt = select(PartyCredential)

        for field, value in filters.items():
            stmt = stmt.where(field == value)

        result = await db.execute(stmt)

        return list(result.scalars().all())

    @staticmethod
    async def get_party_credentials_by_party(
        db: AsyncSession,
        party_id: uuid.UUID
    ) -> List[PartyCredential]:

        return await CredentialService._get_party_credentials_filtered(
            db,
            {PartyCredential.party_id: party_id}
        )

    @staticmethod
    async def get_party_credentials_by_course(
        db: AsyncSession,
        course_id: uuid.UUID
    ) -> List[PartyCredential]:

        return await CredentialService._get_party_credentials_filtered(
            db,
            {PartyCredential.course_id: course_id}
        )

    @staticmethod
    async def get_party_credential(
        db: AsyncSession,
        credential_id: uuid.UUID
    ) -> PartyCredential:

        result = await CredentialService._get_party_credentials_filtered(
            db,
            {PartyCredential.credential_id: credential_id}
        )

        return result[0] if result else None

    @staticmethod
    async def create_party_credential(
        db: AsyncSession,
        party_credential_in: PartyCredentialCreate
    ) -> PartyCredential:
        db_credential = PartyCredential(**party_credential_in.model_dump())
        db.add(db_credential)
        await db.commit()
        await db.refresh(db_credential)
        return db_credential

    @staticmethod
    async def update_party_credential(
        db: AsyncSession,
        credential_id: uuid.UUID,
        party_credential_in: PartyCredentialUpdate
    ) -> PartyCredential:
        db_credential = await CredentialService.get_party_credential(db, credential_id)
        update_data: PartyCredentialUpdate = party_credential_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_credential, field, value)

        db.add(db_credential)
        await db.commit()
        await db.refresh(db_credential)
        return db_credential