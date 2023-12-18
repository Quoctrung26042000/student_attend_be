from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, constr, validator

from app.models.domain.account import Account
from app.models.schemas.rwschema import RWSchema


class AccountInLogin(RWSchema):
    email: Optional[EmailStr]
    password: constr(max_length=10)

class AccountInCreate(AccountInLogin):
    username: str
    role : int
    teacher_id : int


class AccountInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class AccountWithToken(Account):
    token: str
    teacher_name :Optional[str] = ""

class AccountTeacher(Account):
    teacher_name: str

class AccountInResponse(RWSchema):
    data: AccountWithToken
