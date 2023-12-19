from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, conint, validator, constr
from app.models.domain.base_infor import Base, BaseInfor
# from app.models.domain.student import StudentInDB
# from app.models.schemas.rwschema import RWSchema

from enum import IntEnum

class GenderEnum(IntEnum):
    male = 1
    female = 2

class StudentInCreate(BaseInfor):
    gender: GenderEnum
    classId: conint(ge=1)

class StudentInUpdate(BaseInfor):
    gender: GenderEnum
    classId: conint(ge=1)
 
class StudentInResponse(BaseInfor):
    gender: GenderEnum
    classId: conint(ge=1)
    className:str

    @classmethod
    def from_create(cls, student_create: StudentInCreate):
        return cls(
            gender='male' if student_create.gender == GenderEnum.male else 'female',
            classId=student_create.classId
        )

class StudentList(BaseModel):
    data : List[StudentInResponse]
