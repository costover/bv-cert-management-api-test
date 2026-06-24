import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CourseResponse(BaseModel):
    course_id: uuid.UUID
    course_name: str
    description: str | None
    status_id: str
    created_date: datetime
    deadline_type_id: str | None
    deadline_date: datetime | None
    deadline_relative: int | None
    deadline_relative_uom_id: str | None
    eleap_course_id: str | None


class CourseCreate(BaseModel):
    course_name: str = Field(
        max_length=255
    )
    description: str | None = Field(
        max_length=255
    )
    status_id: str = Field(
        max_length=20
    )
    deadline_type_id: str | None = Field(
        default=None,
        max_length=20
    )
    deadline_date: datetime | None = Field(
        default=None
    )
    deadline_relative: int | None = Field(
        default=None
    )
    deadline_relative_uom_id: str | None = Field(
        default=None
    )
    eleap_course_id: str | None = Field(
        default=None
    )


class CourseUpdate(BaseModel):
    course_name: str = Field(
        max_length=255
    )
    description: str | None = Field(
        max_length=255
    )
    status_id: str = Field(
        max_length=20
    )
    deadline_type_id: str | None = Field(
        default=None,
        max_length=20
    )
    deadline_date: datetime | None = Field(
        default=None
    )
    deadline_relative: int | None = Field(
        default=None
    )
    deadline_relative_uom_id: str | None = Field(
        default=None
    )
    eleap_course_id: str | None = Field(
        default=None
    )


class CourseMemberResponse(BaseModel):
    course_member_id: uuid.UUID
    course_id: uuid.UUID
    party_id: uuid.UUID
    status_id: str | None
    start_date: datetime | None
    completion_date: datetime | None


class CourseMemberCreate(BaseModel):
    course_id: uuid.UUID
    party_id: uuid.UUID
    status_id: str | None = Field(
        max_length=20
    )
    start_date: datetime | None
    completion_date: datetime | None


class CourseMemberUpdate(BaseModel):
    course_id: uuid.UUID
    party_id: uuid.UUID
    status_id: str | None = Field(
        max_length=20
    )
    start_date: datetime | None
    completion_date: datetime | None