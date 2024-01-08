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
        self,
        *,
        username: str,
        email: str,
        password: str,
        role :int,
        teacher_id:int
    ) -> AccountInDB:
        account = AccountInDB(username=username, email=email, role=role, teacher_id=teacher_id)
        account.change_password(password)
        async with self.connection.transaction():
            account_row = await queries.create_new_account(
                self.connection,
                username=account.username,
                email=account.email,
                salt=account.salt,
                hashed_password=account.hashed_password,
                role=account.role,
                teacher_id=account.teacher_id
            )

        return account.copy(update=dict(account_row))
    
    async def teacher_unassigned_account(
        self,
    ):
        async with self.connection.transaction():
            teacher_row = await queries.teacher_unassigned_account(
                self.connection)
        return teacher_row
    
    async def get_accounts(self):
        async with self.connection.transaction():
            accounts_row = await queries.get_accounts(
                self.connection)
        return accounts_row
    

    # async def update_user(  # noqa: WPS211
    #     self,
    #     *,
    #     user: User,
    #     username: Optional[str] = None,
    #     email: Optional[str] = None,
    #     password: Optional[str] = None,
    #     bio: Optional[str] = None,
    #     image: Optional[str] = None,
    # ) -> UserInDB:
    #     user_in_db = await self.get_user_by_username(username=user.username)

    #     user_in_db.username = username or user_in_db.username
    #     user_in_db.email = email or user_in_db.email
    #     user_in_db.bio = bio or user_in_db.bio
    #     user_in_db.image = image or user_in_db.image
    #     if password:
    #         user_in_db.change_password(password)

    #     async with self.connection.transaction():
    #         user_in_db.updated_at = await queries.update_user_by_username(
    #             self.connection,
    #             username=user.username,
    #             new_username=user_in_db.username,
    #             new_email=user_in_db.email,
    #             new_salt=user_in_db.salt,
    #             new_password=user_in_db.hashed_password,
    #             new_bio=user_in_db.bio,
    #             new_image=user_in_db.image,
    #         )

    #     return user_in_db
