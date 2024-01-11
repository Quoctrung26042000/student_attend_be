from typing import Optional, List
from datetime import date, datetime
from enum import IntEnum
from pydantic import BaseModel, validator


class StatusEnum(IntEnum):
    PRESENT = 1
    ABSENT = 2
    LATE = 3
    EXCUSED_ABSENCE = 4


class AttendanceClass(BaseModel):
    id: int
    phone: str
    name: str
    status: Optional[StatusEnum] = 2
    note: Optional[str] = None
    timeCheckIn: Optional[str] = None
    timeCheckOut: Optional[str] = None
    className: Optional[str] = None

    @validator("status")
    def status_is_valid(cls, v):
        status_values = set(item.value for item in StatusEnum)
        if v.value not in status_values:
            raise ValueError("Status must be one of the defined StatusEnum values")
        return v

    def __init__(self, **data):
        if "status" not in data or data["status"] is None:
            data["status"] = StatusEnum.ABSENT
        if "timeCheckIn" in data and isinstance(data["timeCheckIn"], datetime):
            data["timeCheckIn"] = data["timeCheckIn"].strftime("%Y-%m-%d %H:%M:%S")
        if "timeCheckOut" in data and isinstance(data["timeCheckOut"], datetime):
            data["timeCheckOut"] = data["timeCheckOut"].strftime("%Y-%m-%d %H:%M:%S")
        super().__init__(**data)


class AttendanceClassList(BaseModel):
    data: List[AttendanceClass]


class AttendanceStatistics(BaseModel):
    id: int
    grade: str
    classId: int
    className: str
    quantity: int
    present: int
    absenceWithPermission: int
    absenceWithoutPermission: int
    late: int
    homeroomTeacher: int


class AttendanceStatisList(BaseModel):
    data: List
    summary: dict


class AttendanceStatisListV2(BaseModel):
    data: List


class StatictInput(BaseModel):
    # grade_id: Optional[int]
    class_id: Optional[int]
    from_date: Optional[date]
    to_date: Optional[date]


class StudentInUpdate(BaseModel):
    status: int
    note: Optional[str] = ""


class AttendanceAproveAll(BaseModel):
    status: Optional[StatusEnum] = 2
    note: Optional[str] = None
