from typing import Optional, List
from app.resources import strings
from pydantic import BaseModel, EmailStr, HttpUrl, validator, Field, ValidationError, constr
from fastapi.responses import JSONResponse  

from app.models.domain.teacher import Teacher
from app.models.domain.base_infor import Base, BaseInfor
from app.models.schemas.rwschema import RWSchema

class ListOfTeacher(BaseModel):
    teacher: List[Teacher]

class TeacherInCreate(Base):
    name: str
    address: str
    phone: Optional[
        constr(
            strip_whitespace=True,
            min_length=9,
            max_length=15,
        )
    ]

    @validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():  
            raise ValueError("Name must not be empty")
        return v
    
    @validator("address")
    def address_must_not_be_empty(cls, v):
        if not v.strip():  
            raise ValueError("Address must not be empty")
        return v


class TeacherInResponse(BaseModel):
    id: int
    name:str
    homeroomClassId: Optional[int] 
    homeroomClass: Optional[str]
    address: Optional[str] = None
    phone: str

class TeacherInResponseBase(BaseModel):
    value :int
    label :str

class TeacherInResponseCreate(BaseModel):
    name:str
    phone:str
    address:str

class TeacherIsDel(BaseModel):
    id: int


class TeacherList(BaseModel):
    data : List[TeacherInResponse]

class TeacherUnassignedList(BaseModel):
    data : List[TeacherInResponseBase]

class TeacherInUpdate(TeacherInResponse):
    pass