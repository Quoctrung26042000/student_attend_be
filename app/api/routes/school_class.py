from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette import status
from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.school import ClassRepository
from app.models.schemas.school import (
    ClassInfo,
    ClassInRepository,
    ClassInCreate
)
from app.resources import strings
from app.services import jwt
# from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.services.school import check_class_is_taken

router = APIRouter()

@router.get(
    "/class",
    response_model=ClassInfo,
    name="Get:all-class",
)
async def get_all_class(class_repo: ClassRepository = Depends(get_repository(ClassRepository))):
    all_class = await class_repo.get_all_class()
    return ClassInfo(
        data=all_class
    )


@router.post(
    "/class",
    status_code=HTTP_201_CREATED,
    response_model=ClassInRepository,
    name="register:class",
)
async def register_class(
    class_create: ClassInCreate = Body(..., embed=True, alias="class"),
    class_repo: ClassRepository = Depends(get_repository(ClassRepository)),
) -> ClassInRepository:
    if (await check_class_is_taken(class_repo, class_create.class_name)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.CLASS_TAKEN,
        )
    class_created = await class_repo.create_class(**class_create.dict())
    return ClassInRepository(
        data=ClassInCreate(
            class_name=class_created.class_name,
            grade_id=class_created.grade_id
        )
    )

