from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, conint, validator, constr

from enum import IntEnum

class StatusEnum(IntEnum):
    PRESENT = 1
    ABSENT = 2
    LATE = 3
    EXCUSED_ABSENCE = 4

class AttendanceClass(BaseModel):
    id:int
    phone:str
    name:str
    status: StatusEnum
    note:str
    timeCheckIn:str
    timeCheckOut:str


