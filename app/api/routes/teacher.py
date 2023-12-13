from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.teacher import TeacherRepository
from app.models.schemas.teacher import (
    TeacherInCreate,
    TeacherInResponse,
    ListOfTeacher
)
from app.resources import strings
from app.services import jwt
from app.services.authentication import check_email_is_taken, check_username_is_taken

router = APIRouter()

@router.get("/teachers",
    name="profiles:get-profile",)
async def get_teachers(
    teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository)),
):
    teacher_list = await teacher_repo.search_teachers()
    return teacher_list

@router.post(
    "/create_teacher",
    status_code=HTTP_201_CREATED,
    response_model=TeacherInResponse,
    name="register:teacher",
)
async def register_teacher(
    teacher_create: TeacherInCreate = Body(..., embed=True, alias="teacher"),
    teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository)),
) -> TeacherInResponse:
    teacher_created = await teacher_repo.create_teacher(**teacher_create.dict())
    return TeacherInResponse(
        name = teacher_created.name,
        phone = teacher_created.phone,
        homeroom_class = teacher_created.homeroom_class
    )

