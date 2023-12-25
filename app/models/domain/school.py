from typing import Optional

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class GradeInDB(RWModel):
    # id : int
    grade_name: int

class ClassInDB(RWModel, IDModelMixin, DateTimeModelMixin):
    class_name: str
    grade_id : int
    # grade_name:str


class ClassInFor(RWModel):
    id : int
    quantity:int
    homeroomTeacher:int
    phone:str
    class_name: str
    grade_id : int
    grade_name: str
    