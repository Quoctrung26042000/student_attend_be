from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette import status
from fastapi.responses import JSONResponse  


from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.student import StudentRepository
from app.models.schemas.student import (
    StudentInCreate,
    StudentInResponse
)
from app.resources import strings
from app.services import jwt
from app.services.teacher import check_teacher_is_taken, check_phone_is_taken

from typing import Optional, List

router = APIRouter()

@router.post(
    "/student",
    status_code=HTTP_201_CREATED,
    name="register:student",
)
async def register_teacher(
    student_create: StudentInCreate = Body(...,),
    student_repo: StudentRepository = Depends(get_repository(StudentRepository)),
) -> StudentRepository:

    # if await check_teacher_is_taken(teacher_repo, teacher_name=teacher_create.name) == True:
    #     return JSONResponse({"error":strings.TEACHER_EXITS},400)
    
    # if await check_phone_is_taken(teacher_repo, phone=teacher_create.phone) == True:
    #     return JSONResponse({"error":strings.PHONE_EXITS},400)
    
    teacher_created = await student_repo.create_student(**student_create.dict())
 
    return StudentInResponse(
        name = teacher_created.name,
        phone = teacher_created.phone,
        address = teacher_created.address
    )




