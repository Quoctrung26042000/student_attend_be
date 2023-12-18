from typing import Optional
from datetime import date
from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.services import security

from enum import IntEnum

class GenderEnum(IntEnum):
    male = 1
    female = 2

class Student(RWModel):
    name: str
    phone: str
    gender: GenderEnum
    address: Optional[str]
    date_of_birth:date
    class_id:int
    
class StudentInDB(IDModelMixin, DateTimeModelMixin, Student):
    pass

