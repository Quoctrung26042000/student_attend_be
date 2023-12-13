from typing import Optional

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.services import security

class Teacher(RWModel):
    name: str
    phone: str
    homeroom_class: int
    
class TeacherInDB(IDModelMixin, DateTimeModelMixin, Teacher):
    pass

