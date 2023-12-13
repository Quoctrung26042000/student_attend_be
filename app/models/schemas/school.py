from typing import Optional, List

from pydantic import BaseModel, EmailStr, HttpUrl, conint, validator

from app.models.domain.school import GradeInDB, ClassInDB
from app.models.schemas.rwschema import RWSchema



class GradeInCreate(RWSchema):
    grade_name: conint(ge=1, le=12)

class GradeInRepository(GradeInCreate):
    pass


class GradeInfo(RWSchema):
    data : List[GradeInDB]




class ClassInfo(RWSchema):
    data : List[ClassInDB]

class ClassInCreate(RWSchema):
    class_name :str
    grade_id : int

    @validator('class_name')
    def uppercase_class_name(cls, value):
        return value.upper()

class ClassInRepository(RWSchema):
    data : ClassInDB