from typing import Optional
from datetime import date, datetime
from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.services import security
from pydantic import BaseModel, EmailStr, HttpUrl, conint, validator, constr
from app.models.domain.base_infor import Base, BaseInfor

from enum import IntEnum


class GenderEnum(IntEnum):
    male = 1
    female = 2


class Student(RWModel, BaseInfor):
    gender: GenderEnum
    classId: Optional[int] = None


class StudentInDB(IDModelMixin, DateTimeModelMixin, Student):
    pass
