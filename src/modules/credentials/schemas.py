import uuid
from datetime import datetime

from pydantic import BaseModel

from src.core.schema import ApiModel


class PartyCredentialResponse(ApiModel):
    credential_id: uuid.UUID
    party_id: uuid.UUID
    course_id: uuid.UUID
    from_date: datetime | None
    thru_date: datetime | None


class PartyCredentialCreate(ApiModel):
    party_id: uuid.UUID
    course_id: uuid.UUID
    from_date: datetime | None
    thru_date: datetime | None


class PartyCredentialUpdate(ApiModel):
    party_id: uuid.UUID
    course_id: uuid.UUID
    from_date: datetime | None
    thru_date: datetime | None