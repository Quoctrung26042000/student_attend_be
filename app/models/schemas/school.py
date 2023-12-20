from typing import Optional, List

from pydantic import BaseModel, EmailStr, HttpUrl, conint, validator

from app.models.domain.school import GradeInDB, ClassInDB
from app.models.schemas.rwschema import RWSchema



class GradeInCreate(RWSchema):
    grade_name: conint(ge=1, le=12)

class GradeInRepository(GradeInCreate):
    pass


class  GradeInfo(BaseModel):
    value: int
    label: str
    
class GradeList(BaseModel):
    data : List[GradeInfo]

class ClassInfoBase(BaseModel):
    id:int
    className:str
    gradeId:int
    gradeName:str
    quantity:int
    teacher_id:Optional[int] = None
    homeroomTeacher:Optional[str] = None

class ClassSelection(BaseModel):
    value: int
    label:str


class ClassInfo(BaseModel):
    data : List[ClassInfoBase]


class ClassListSelection(BaseModel):
    data : List[ClassSelection]

class ClassDel(BaseModel):
    id : int

class ClassInCreate(RWSchema):
    class_name :Optional[str] = None
    grade_id : Optional[int] = None
    teacher_id: Optional[int] = None
    @validator('class_name')
    def uppercase_class_name(cls, value):
        return value.upper()

class ClassInRepository(RWSchema):
    data : ClassInDB

class ClassRepositoryCreate(BaseModel):
    class_name:str
    grade_id:int
    teacher_id:int