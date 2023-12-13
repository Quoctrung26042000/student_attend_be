from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from app.models.domain.account import Account
from app.models.schemas.rwschema import RWSchema


class AccountInLogin(RWSchema):
    email: EmailStr
    password: str


class AccountInCreate(AccountInLogin):
    username: str
    role : int


class AccountInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class AccountWithToken(Account):
    token: str


class AccountInResponse(RWSchema):
    account: AccountWithToken
