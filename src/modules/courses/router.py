import uuid
from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.modules.courses.schemas import CourseResponse, CourseCreate, CourseUpdate, CourseMemberResponse, \
    CourseMemberCreate, CourseMemberUpdate
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


@router.get("/members/course/{course_id}", response_model=list[CourseMemberResponse], status_code=status.HTTP_200_OK)
async def get_course_members_by_course(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    return await CourseService.get_course_members_by_course(db, course_id)


@router.get("/members/party/{party_id}", response_model=list[CourseMemberResponse], status_code=status.HTTP_200_OK)
async def get_course_members_by_party(
    party_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    return await CourseService.get_course_members_by_party(db, party_id)


@router.get("/members/{course_member_id}", response_model=CourseMemberResponse, status_code=status.HTTP_200_OK)
async def get_course_member(
    course_member_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    return await CourseService.get_course_member(db, course_member_id)


@router.post("/members", response_model=CourseMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_course_member(
    course_member_in: CourseMemberCreate,
    db: AsyncSession = Depends(get_db_session)
):
    return await CourseService.create_course_member(db, course_member_in)


@router.patch("/members", response_model=CourseMemberResponse, status_code=status.HTTP_200_OK)
async def update_course_member(
    course_member_id: uuid.UUID,
    course_member_in: CourseMemberUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    return await CourseService.update_course_member(db, course_member_id, course_member_in)