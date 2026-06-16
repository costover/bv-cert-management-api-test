import uuid
from datetime import datetime

from pydantic import BaseModel

class CourseCreate(BaseModel):
    course_name: str
    description: str | None
    status_id: str
    deadline_type_id: str
    deadline_date: datetime | None
    deadline_relative: int | None
    deadline_relative_uom_id: str | None
    eleap_course_id: str | None

class CourseResponse(BaseModel):
    course_id: uuid.UUID
    course_name: str
    description: str | None
    status_id: str
    created_date: datetime
    deadline_type_id: str
    deadline_date: datetime | None
    deadline_relative: int | None
    deadline_relative_uom_id: str | None
    eleap_course_id: str | None