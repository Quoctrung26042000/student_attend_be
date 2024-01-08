from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, validator, constr

class Base(BaseModel):
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
    

    

class BaseInfor(Base):
    dateOfBirth: date
    @validator("dateOfBirth", pre=True)
    def parse_birthdate(cls, value):
        if not value:
            raise ValueError("Date of birth must not be empty")
        if isinstance(value, str):
            return datetime.strptime(value, "%d-%m-%Y").date()
        return value

