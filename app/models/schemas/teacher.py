from typing import Optional, List
from app.resources import strings
from pydantic import BaseModel, EmailStr, HttpUrl, validator, Field, ValidationError
from fastapi.responses import JSONResponse  

from app.models.domain.teacher import Teacher
from app.models.schemas.rwschema import RWSchema

class ListOfTeacher(BaseModel):
    teacher: List[Teacher]

class TeacherInCreate(RWSchema):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


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