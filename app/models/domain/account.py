from typing import Optional

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.services import security


class Account(RWModel):
    username: str
    email: str
    role : int
    teacher_id: Optional[int]


class AccountInDB(IDModelMixin, DateTimeModelMixin, Account):
    salt: str = ""
    hashed_password: str = ""
    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)

class AccounInforInDB(IDModelMixin, DateTimeModelMixin, Account):
    salt: str = ""
    hashed_password: str = ""
    teacher_name : Optional[str] = None
    classId:Optional[int] = None    
    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)