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
    className: str
    dateOfBirth: str
    gradeId: int

    @validator("dateOfBirth", pre=True)
    def parse_birthdate(cls, value):
        if not value:
            raise ValueError("Date of birth must not be empty")

        if isinstance(value, date):
            return value.strftime(
                "%d/%m/%Y"
            )  # If it's already a date object, no need to parse

        # Parse the date if it's a string in the 'D/M/Y' format
        return datetime.strptime(value, "%d/%m/%Y").date()


class StudentList(BaseModel):
    data: List[StudentInResponse]
