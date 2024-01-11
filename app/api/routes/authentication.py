from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from fastapi.responses import JSONResponse

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.account import AccountRepository
from app.db.repositories.account import Account
from app.models.schemas.account import (
    AccountInCreate,
    AccountInLogin,
    AccountInResponse,
    AccountWithToken,
    AccountInUpdate,
)
from app.api.dependencies.authentication import get_current_user_authorizer
from app.resources import strings
from app.services import jwt
from app.services.authentication import (
    check_email_is_taken,
    check_username_is_taken,
    check_account_is_taken,
    check_email_account_is_taken,
)

router = APIRouter()


@router.post("/login", response_model=AccountInResponse, name="auth:login")
async def login(
    user_login: AccountInLogin = Body(),
    users_repo: AccountRepository = Depends(get_repository(AccountRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> AccountInResponse:
    wrong_login_error = JSONResponse({"error": strings.INCORRECT_LOGIN_INPUT}, 400)

    try:
        user = await users_repo.get_account_by_email(email=user_login.email)

        if user.teacher_name is None:
            user.teacher_name = "Admin"
    except Exception as e:
        return wrong_login_error

    if not user.check_password(user_login.password):
        return wrong_login_error

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return AccountInResponse(
        data=AccountWithToken(
            username=user.username,
            email=user.email,
            token=token,
            role=user.role,
            teacher_id=user.teacher_id,
            teacher_name=user.teacher_name,
            classId=user.classId,
            className=user.className,
        ),
    )


@router.post(
    "/account",
    response_model=AccountInResponse,
    name="auth:register",
)
async def register(
    user_create: AccountInCreate = Body(..., embed=False),
    users_repo: AccountRepository = Depends(get_repository(AccountRepository)),
    # user: Account = Depends(get_current_user_authorizer()),
    settings: AppSettings = Depends(get_app_settings),
) -> AccountInResponse:
    # if user.role == 1 :
    #     return JSONResponse({"error":strings.PER_DENIED},400)
    user_create.user_name = user_create.email.split("@")[0]
    print(user_create)
    # if await check_account_is_taken(users_repo, user_create.username):
    #     return JSONResponse({"error":strings.USERNAME_TAKEN},400)
    # user_create.username = user_create.email.split("@")[0]
    if await check_email_account_is_taken(users_repo, user_create.email):
        return JSONResponse({"error": strings.EMAIL_TAKEN}, 400)

    user = await users_repo.create_account(**user_create.dict())
    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return AccountInResponse(
        data=AccountWithToken(
            username=user.username,
            email=user.email,
            role=user.role,
            token=token,
            teacher_id=user.teacher_id,
            # className=user.className
        ),
    )


@router.get("/me")
async def protected_route(
    token: str,
    settings: AppSettings = Depends(get_app_settings),
    users_repo: AccountRepository = Depends(get_repository(AccountRepository)),
):
    try:
        username = jwt.get_username_from_token(
            token,
            str(settings.secret_key.get_secret_value()),
        )
        account = await users_repo.get_account_by_username(username=username)
        return AccountInResponse(
            data=AccountWithToken(
                username=account.username,
                email=account.email,
                role=account.role,
                token=token,
                teacher_id=account.teacher_id,
            ),
        )
    except Exception as e:
        return JSONResponse({"errors": strings.VERIFY_TOKEN}, 400)


@router.get("/school/account/teacher_unassigned")
async def teacher_unassigned(
    users_repo: AccountRepository = Depends(get_repository(AccountRepository)),
):
    try:
        data_object = []
        teacher_unassigned_account = await users_repo.teacher_unassigned_account()

        for item in teacher_unassigned_account:
            data_object.append(
                {
                    "value": item["id"],
                    "label": item["username"],
                }
            )
        return JSONResponse({"data": data_object}, 200)
    except Exception as e:
        return JSONResponse({"errors": strings.VERIFY_TOKEN}, 400)


@router.get("/account")
async def get_account(
    users_repo: AccountRepository = Depends(get_repository(AccountRepository)),
):
    accounts = await users_repo.get_accounts()

    return {"data": accounts}


@router.delete("/account/{account_id}")
async def get_account(
    account_id: int,
    users_repo: AccountRepository = Depends(get_repository(AccountRepository)),
):
    account_del = await users_repo.delete_account_by_id(account_id)

    return account_del


@router.patch("/account/{account_id}")
async def update_account(
    account_id: int,
    user_update: AccountInUpdate = Body(..., embed=False),
    users_repo: AccountRepository = Depends(get_repository(AccountRepository)),
):
    user_update.user_name = user_update.email.split("@")[0]

    account_update_id = await users_repo.update_account_by_id(
        account_id=account_id, data_object=user_update
    )

    return account_update_id
