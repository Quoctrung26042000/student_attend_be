from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette import status
from fastapi.responses import JSONResponse  


from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.teacher import TeacherRepository
from app.models.schemas.teacher import (
    TeacherInCreate,
    TeacherInResponse,
    TeacherInResponseCreate,
    ListOfTeacher,
    TeacherList
)
from app.resources import strings
from app.services import jwt
from app.services.teacher import check_teacher_is_taken, check_phone_is_taken

from typing import Optional, List

router = APIRouter()

@router.get("/teacher",
    name="profiles:get-profile",)
async def get_teachers(
    teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository)),
):
    teacher_list = await teacher_repo.search_teachers()
    data_object = []
    for item in teacher_list :
        teacher = {
            "id": item["id"],
            "name": item["username"],
            "homeroomClass": item["class_name"],
            "homeroomClassId": item["homeroom_class_id"],
            "address": item["address"],
            "phone": item["phone"]
        }
        data_object.append(teacher)
    return JSONResponse({"data": data_object}, 200)
    

@router.get("/teacher/unassigned",
    name="profiles:get-teacher-unassigned-profile",)
async def get_teacher_unassigned(
    teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository)),
):
    teacher_list = await teacher_repo.search_teacher_unassigned()
    data_object = []
    for item in teacher_list :
        teacher = {
            "id": item["id"],
            "name": item["username"],
        }
        data_object.append(teacher)
    return JSONResponse({"data": data_object}, 200)

@router.post(
    "/teacher",
    status_code=HTTP_201_CREATED,
    name="register:teacher",
)
async def register_teacher(
    teacher_create: TeacherInCreate = Body(...,),
    teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository)),
) -> TeacherInResponse:
    
    missing_fields = [field for field, value in teacher_create.dict().items() if value is ""]
    error_msgs =[]
    if missing_fields:
        for field in missing_fields:
            error = {field:f"Phải nhập {field}"}
            error_msgs.append(error)
        return JSONResponse({"errors": error_msgs}, status_code=400)
    
    if await check_teacher_is_taken(teacher_repo, teacher_name=teacher_create.name) == True:
        return JSONResponse({"error":strings.TEACHER_EXITS},400)
    
    if await check_phone_is_taken(teacher_repo, phone=teacher_create.phone) == True:
        return JSONResponse({"error":strings.PHONE_EXITS},400)
    
    teacher_created = await teacher_repo.create_teacher(**teacher_create.dict())
 
    return TeacherInResponseCreate(
        name = teacher_created.name,
        phone = teacher_created.phone,
        # homeroom_class = teacher_created.homeroom_class,
        address = teacher_created.address
    )

