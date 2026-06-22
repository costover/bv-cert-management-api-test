import uuid

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.modules.courses.schemas import CourseResponse, CourseCreate, CourseUpdate
from src.modules.courses.service import CourseService

router = APIRouter()

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db_session)
):
    return await CourseService.create_course(db, course_in)

@router.patch("/", response_model=CourseResponse, status_code=status.HTTP_200_OK)
async def update_course(
    course_id: uuid.UUID,
    course_in: CourseUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    return await CourseService.update_course(db, course_id, course_in)

@router.get("/{course_id}", response_model=CourseResponse, status_code=status.HTTP_200_OK)
async def get_course(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    return await CourseService.get_course(db, course_id)