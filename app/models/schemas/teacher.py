from typing import Optional, List

from pydantic import BaseModel, EmailStr, HttpUrl

from app.models.domain.teacher import Teacher
from app.models.schemas.rwschema import RWSchema

class ListOfTeacher(BaseModel):
    teacher: List[Teacher]

class TeacherInCreate(RWSchema):
    name: str
    phone: str
    homeroom_class: int


class TeacherInResponse(Teacher):
    pass
