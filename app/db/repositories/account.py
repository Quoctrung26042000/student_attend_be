from typing import Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.account import Account, AccountInDB, AccounInforInDB


class AccountRepository(BaseRepository):
    async def get_account_by_email(self, *, email: str) -> AccounInforInDB:
        user_row = await queries.get_account_by_email(self.connection, email=email)
        if user_row:
            return AccounInforInDB(**user_row)
        raise EntityDoesNotExist("account with email {0} does not exist".format(email))

    async def get_account_by_username(self, *, username: str) -> AccounInforInDB:
        user_row = await queries.get_account_by_username(
            self.connection,
            username=username,
        )
        if user_row:
            return AccounInforInDB(**user_row)

        raise EntityDoesNotExist(
            "account with username {0} does not exist".format(username),
        )

    async def create_account(
        self, *, user_name: str, email: str, password: str, role: int, teacher_id: int
    ) -> AccountInDB:
        account = AccountInDB(
            username=user_name, email=email, role=role, teacher_id=teacher_id
        )
        account.change_password(password)
        async with self.connection.transaction():
            account_row = await queries.create_new_account(
                self.connection,
                username=account.username,
                email=account.email,
                salt=account.salt,
                hashed_password=account.hashed_password,
                role=account.role,
                teacher_id=account.teacher_id,
            )

        return account.copy(update=dict(account_row))

    async def teacher_unassigned_account(
        self,
    ):
        async with self.connection.transaction():
            teacher_row = await queries.teacher_unassigned_account(self.connection)
        return teacher_row

    async def get_accounts(self):
        async with self.connection.transaction():
            accounts_row = await queries.get_accounts(self.connection)
        return accounts_row

    async def delete_account_by_id(self, id):
        async with self.connection.transaction():
            accounts_id = await queries.delete_account_by_id(self.connection, id)
        return accounts_id

    async def update_account_by_id(
        self, *, user_name: str, email: str, password: str, role: int, teacher_id: int
    ):
        account = AccountInDB(
            username=user_name, email=email, role=role, teacher_id=teacher_id
        )
        async with self.connection.transaction():
            accounts_id = await queries.delete_account_by_id(self.connection, id)
        return accounts_id
