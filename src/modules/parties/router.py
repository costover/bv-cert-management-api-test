import uuid

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user, get_db_session
from src.modules.parties.schemas import PartyResponse, PartyCreate, PartyUpdate, PartyRequest
from src.modules.parties.service import PartyService

router = APIRouter()

@router.post("/", response_model=PartyResponse, status_code=status.HTTP_201_CREATED)
async def create_party(
    party_in: PartyCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user)
):
    return await PartyService.create_party(db, party_in)


@router.patch("/", response_model=PartyResponse, status_code=status.HTTP_200_OK)
async def update_party(
    party_id: uuid.UUID,
    party_in: PartyUpdate,
    db: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user)
):
    return await PartyService.update_party(db, party_id, party_in)


@router.get("/", response_model=PartyResponse, status_code=status.HTTP_200_OK)
async def get_party(
    party_id: uuid.UUID = Query(alias="partyId"),
    db: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user)
):
    return await PartyService.get_party(db, party_id)