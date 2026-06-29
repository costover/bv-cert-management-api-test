import uuid

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user, get_db_session
from src.modules.credentials.schemas import PartyCredentialResponse, PartyCredentialCreate, PartyCredentialUpdate
from src.modules.credentials.service import CredentialService

router = APIRouter()

@router.get("/", response_model=PartyCredentialResponse, status_code=status.HTTP_200_OK)
async def get_party_credential(
    credential_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user)
):
    return await CredentialService.get_party_credential(db, credential_id)

@router.get("/party/{party_id}", response_model=list[PartyCredentialResponse], status_code=status.HTTP_200_OK)
async def get_party_credentials_by_party(
    party_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user)
):
    return await CredentialService.get_party_credentials_by_party(db, party_id)

@router.get("/course/{course_id}", response_model=list[PartyCredentialResponse], status_code=status.HTTP_200_OK)
async def get_party_credentials_by_course(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user)
):
    return await CredentialService.get_party_credentials_by_course(db, course_id)

@router.post("/", response_model=PartyCredentialResponse, status_code=status.HTTP_201_CREATED)
async def create_party_credential(
    party_credential_in: PartyCredentialCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user)
):
    return await CredentialService.create_party_credential(db, party_credential_in)

@router.patch("/", response_model=PartyCredentialResponse, status_code=status.HTTP_201_CREATED)
async def update_party_credential(
    credential_id: uuid.UUID,
    party_credential_in: PartyCredentialUpdate,
    db: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user)
):
    return await CredentialService.update_party_credential(db, credential_id, party_credential_in)