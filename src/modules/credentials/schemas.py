import uuid
from datetime import datetime

from pydantic import BaseModel


class PartyCredentialResponse(BaseModel):
    credential_id: uuid.UUID
    party_id: uuid.UUID
    course_id: uuid.UUID
    from_date: datetime | None
    thru_date: datetime | None


class PartyCredentialCreate(BaseModel):
    party_id: uuid.UUID
    course_id: uuid.UUID
    from_date: datetime | None
    thru_date: datetime | None


class PartyCredentialUpdate(BaseModel):
    party_id: uuid.UUID
    course_id: uuid.UUID
    from_date: datetime | None
    thru_date: datetime | None