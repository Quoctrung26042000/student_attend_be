from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, constr, validator

from app.models.domain.account import Account
from app.models.schemas.rwschema import RWSchema


class AccountInLogin(RWSchema):
    email: Optional[EmailStr]
    password: constr(max_length=10)


class AccountInCreate(AccountInLogin):
    user_name: str
    role: int
    teacher_id: int

    def extract_name_from_email(self, email: EmailStr) -> str:
        self.user_name = email.split("@")[0]


class AccountInUpdate(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    role: Optional[int] = 1
    user_name: Optional[str] = ""


class AccountWithToken(Account):
    token: str
    teacher_name: Optional[str] = ""
    classId: Optional[int] = None
    className: Optional[str] = None


class AccountTeacher(Account):
    teacher_name: str


class AccountInResponse(RWSchema):
    data: AccountWithToken
