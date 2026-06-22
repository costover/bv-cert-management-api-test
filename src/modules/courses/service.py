import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.courses import Course
from src.modules.courses.schemas import CourseCreate, CourseUpdate


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