import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.courses.models import Course
from src.modules.courses.schemas import CourseCreate


class CourseService:
    @staticmethod
    async def create_course(db:AsyncSession, course_in: CourseCreate):
        existing_course = await db.scalar(select(Course).where(Course.course_name == course_in.course_name))
        if existing_course:
            raise HTTPException(status_code=400, detail="Course with this name already exists")
        # course_in.deadline_date = course_in.deadline_date.replace(tzinfo=ZoneInfo("UTC"))
        db_course = Course(**course_in.model_dump())
        db.add(db_course)
        await db.commit()
        await db.refresh(db_course)
        return db_course


    @staticmethod
    async def get_course(db: AsyncSession, course_id: uuid.UUID):
        course = await db.get(Course, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course