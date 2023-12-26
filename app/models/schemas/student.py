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
    classId: Optional[conint(ge=0)] = None

    @validator("address")
    def address_must_not_be_empty(cls, v):
        if not v.strip():  
            raise ValueError("Address must not be empty")
        return v
 
class StudentInResponse(Base):
    id: int
    gender: GenderEnum
    classId: conint(ge=1)
    className:str
    dateOfBirth:date
    gradeId:int

    # @classmethod
    # def from_create(cls, student_create: StudentInCreate):
    #     parsed_date = datetime.strptime(student_create.dateOfBirth, '%Y-%m-%d')
    #     formatted_date = parsed_date.strftime('%d-%m-%Y')
    #     return cls(
    #         gender='male' if student_create.gender == GenderEnum.male else 'female',
    #         classId=student_create.classId,
    #         dateOfBirth=formatted_date
    #     )

class StudentList(BaseModel):
    data : List[StudentInResponse]
