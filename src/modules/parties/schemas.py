import uuid

from pydantic import BaseModel


class PartyCreate(BaseModel):
    party_type_id: str
    status_id: str
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    email_address: str | None
    description: str | None
    eleap_user_id: str | None


class PartyUpdate(BaseModel):
    party_type_id: str
    status_id: str
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    email_address: str | None
    description: str | None
    eleap_user_id: str | None


class PartyResponse(BaseModel):
    party_id: uuid.UUID
    party_type_id: str
    status_id: str
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    email_address: str | None
    description: str | None
    eleap_user_id: str | None