from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.users import UsersRepository
from app.db.repositories.account import AccountRepository
from app.db.repositories.account import Account
from app.models.schemas.users import (
    UserInCreate,
    UserInLogin,
    UserInResponse,
    UserWithToken,
)
from app.models.schemas.account import (
    AccountInCreate,
    AccountInLogin,
    AccountInResponse,
    AccountWithToken,
)
from app.api.dependencies.authentication import get_current_user_authorizer
from app.resources import strings
from app.services import jwt
from app.services.authentication import( check_email_is_taken, check_username_is_taken
                , check_account_is_taken,  check_email_account_is_taken)

router = APIRouter()


@router.post("/login", response_model=AccountInResponse, name="auth:login")
async def login(
    user_login: AccountInLogin = Body(..., embed=True, alias="account"),
    users_repo: AccountRepository = Depends(get_repository(AccountRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> AccountInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT,
    )

    try:
        user = await users_repo.get_account_by_email(email=user_login.email)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return AccountInResponse(
        account=AccountWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token,
            role = user.role
        ),
    )

@router.post(
    "/account",
    status_code=HTTP_201_CREATED,
    response_model=AccountInResponse,
    name="auth:register",
)
async def register(
    user_create: AccountInCreate = Body(..., embed=True, alias="register:account"),
    users_repo: AccountRepository = Depends(get_repository(AccountRepository)),
    # user: Account = Depends(get_current_user_authorizer()),
    settings: AppSettings = Depends(get_app_settings),
) -> AccountInResponse:
    if await check_account_is_taken(users_repo, user_create.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )

    if await check_email_account_is_taken(users_repo, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )
    
    user = await users_repo.create_account(**user_create.dict())

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return AccountInResponse(
        account=AccountWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token,
            role = user.role
        ),
    )



# @router.post(
#     "",
#     status_code=HTTP_201_CREATED,
#     response_model=UserInResponse,
#     name="auth:register",
# )
# async def register(
#     user_create: UserInCreate = Body(..., embed=True, alias="user"),
#     users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
#     settings: AppSettings = Depends(get_app_settings),
# ) -> UserInResponse:
#     if await check_username_is_taken(users_repo, user_create.username):
#         raise HTTPException(
#             status_code=HTTP_400_BAD_REQUEST,
#             detail=strings.USERNAME_TAKEN,
#         )

#     if await check_email_is_taken(users_repo, user_create.email):
#         raise HTTPException(
#             status_code=HTTP_400_BAD_REQUEST,
#             detail=strings.EMAIL_TAKEN,
#         )

#     user = await users_repo.create_user(**user_create.dict())

#     token = jwt.create_access_token_for_user(
#         user,
#         str(settings.secret_key.get_secret_value()),
#     )
#     return UserInResponse(
#         user=UserWithToken(
#             username=user.username,
#             email=user.email,
#             bio=user.bio,
#             image=user.image,
#             token=token,
#         ),
#     )
