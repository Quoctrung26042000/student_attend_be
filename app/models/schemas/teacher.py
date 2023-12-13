from typing import Optional, List

from pydantic import BaseModel, EmailStr, HttpUrl, validator
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
    homeroomClass:str
    address:str
    phone:str

class TeacherInResponseCreate(BaseModel):
    name : str
    phone :str
    address:str

class TeacherList(BaseModel):
    data : List[TeacherInResponse]