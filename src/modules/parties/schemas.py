import uuid

from pydantic import BaseModel

from src.core.schema import ApiModel


class PartyRequest(ApiModel):
    party_id: uuid.UUID

class PartyCreate(ApiModel):
    party_type_id: str
    status_id: str
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    email_address: str | None
    description: str | None
    eleap_user_id: str | None


class PartyUpdate(ApiModel):
    party_type_id: str
    status_id: str
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    email_address: str | None
    description: str | None
    eleap_user_id: str | None


class PartyResponse(ApiModel):
    party_id: uuid.UUID
    party_type_id: str
    status_id: str
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    email_address: str | None
    description: str | None
    eleap_user_id: str | None