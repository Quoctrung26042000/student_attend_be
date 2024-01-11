from typing import Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.account import (
    Account,
    AccountInDB,
    AccounInforInDB,
    AccountInUpdate,
)


class AccountRepository(BaseRepository):
    async def get_account_by_email(self, *, email: str) -> AccounInforInDB:
        user_row = await queries.get_account_by_email(self.connection, email=email)
        if user_row:
            return AccounInforInDB(**user_row)
        raise EntityDoesNotExist("account with email {0} does not exist".format(email))

    async def get_account_by_id(self, *, id: int) -> AccounInforInDB:
        user_row = await queries.get_account_by_id(self.connection, id=id)
        if user_row:
            return AccounInforInDB(**user_row)
        raise EntityDoesNotExist("account with Id {0} does not exist".format(id))

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

    async def update_account_by_id(self, *, account_id: int, data_object):
        current_account = await self.get_account_by_id(id=account_id)

        account_update = AccountInUpdate(
            username=data_object.user_name,
            email=data_object.email,
            role=data_object.role,
        )

        if data_object.password:
            account_update.change_password(data_object.password)
        else:
            account_update.salt = current_account.salt
            account_update.hashed_password = current_account.hashed_password

        async with self.connection.transaction():
            accounts_id = await queries.update_account_by_id(
                self.connection,
                account_id=account_id,
                new_username=account_update.username,
                new_email=account_update.email,
                new_hash_password=account_update.hashed_password,
                new_salt=account_update.salt
            )
        return accounts_id
