import uuid
from typing import List, Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from src.core.models.courses import Course, CourseMember
from src.modules.courses.schemas import CourseCreate, CourseUpdate, CourseMemberCreate, CourseMemberUpdate


class CourseService:
    @staticmethod
    async def create_course(
        db:AsyncSession,
        course_in: CourseCreate
    ) -> Course:
        existing_course = await db.scalar(select(Course).where(Course.course_name == course_in.course_name))
        if existing_course:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course with this name already exists")
        db_course = Course(**course_in.model_dump())
        db.add(db_course)
        await db.commit()
        await db.refresh(db_course)
        return db_course

    @staticmethod
    async def update_course(
        db:AsyncSession,
        course_id: uuid.UUID,
        course_in: CourseUpdate
    ) -> Course:
        db_course: Course = await CourseService.get_course(db, course_id)
        update_data: CourseUpdate = course_in.model_dump(exclude_unset=True)

        if "course_name" in update_data and update_data["course_name"] != db_course.course_name:
            existing_course = await db.scalar(
                select(Course).where(Course.course_name == update_data["course_name"])
            )
            if existing_course:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course with this name already exists")

        for field, value in update_data.items():
            setattr(db_course, field, value)

        db.add(db_course)
        await db.commit()
        await db.refresh(db_course)

        return db_course

    @staticmethod
    async def get_course(
        db: AsyncSession,
        course_id: uuid.UUID
    ) -> Course:
        course = await db.scalar(select(Course).where(Course.course_id == course_id))
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        return course

    @staticmethod
    async def get_all_courses(db: AsyncSession) -> List[Course]:
        result = await db.execute(select(Course))
        return list(result.scalars().all())

    @staticmethod
    async def _get_course_members_filtered(
        db: AsyncSession,
        filters: dict[InstrumentedAttribute, Any]
    ) -> List[CourseMember]:

        stmt = select(CourseMember)

        for field, value in filters.items():
            stmt = stmt.where(field == value)

        result = await db.execute(stmt)

        return list(result.scalars().all())

    @staticmethod
    async def get_course_members_by_party(
        db: AsyncSession,
        party_id: uuid.UUID
    ) -> List[CourseMember]:

        return await CourseService._get_course_members_filtered(
            db,
            {CourseMember.party_id: party_id}
        )

    @staticmethod
    async def get_course_members_by_course(
            db: AsyncSession,
            course_id: uuid.UUID
    ) -> List[CourseMember]:

        return await CourseService._get_course_members_filtered(
            db,
            {CourseMember.course_id: course_id}
        )

    @staticmethod
    async def get_course_member(
        db: AsyncSession,
        course_member_id: uuid.UUID
    ) -> CourseMember:

        result = await CourseService._get_course_members_filtered(
            db,
            {CourseMember.course_member_id: course_member_id}
        )

        return result[0] if result else None

    @staticmethod
    async def create_course_member(
        db: AsyncSession,
        course_member_in: CourseMemberCreate
    ) -> CourseMember:
        db_course_member = CourseMember(**course_member_in.model_dump())
        db.add(db_course_member)
        await db.commit()
        await db.refresh(db_course_member)
        return db_course_member

    @staticmethod
    async def update_course_member(
        db: AsyncSession,
        course_member_id: uuid.UUID,
        course_member_in: CourseMemberUpdate
    ) -> CourseMember:
        db_course_member: CourseMember = await CourseService.get_course_member(db, course_member_id)
        update_data: CourseMemberUpdate = course_member_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_course_member, field, value)

        db.add(db_course_member)
        await db.commit()
        await db.refresh(db_course_member)

        return db_course_member