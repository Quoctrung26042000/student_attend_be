from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, HttpUrl, conint, validator

from app.models.domain.student import StudentInDB
from app.models.schemas.rwschema import RWSchema

from enum import IntEnum



class GenderEnum(IntEnum):
    male = 1
    female = 2

class StudentInCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: GenderEnum
    address: str
    class_id: conint(ge=1)
    phone :str

    @validator("date_of_birth", pre=True, check_fields=False)
    def parse_birthdate(cls, value):
        return datetime.strptime(value, "%Y-%m-%d").date()

class StudentInResponse(BaseModel):
    name: str
    date_of_birth: date
    gender: GenderEnum
    address: str
    class_id: conint(ge=1)
