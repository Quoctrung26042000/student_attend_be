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
    TeacherList,
    TeacherInResponseBase,
    TeacherInUpdate,
    TeacherIsDel,
    TeacherUnassignedList

)
from fastapi.encoders import jsonable_encoder
from app.resources import strings
from app.services import jwt
from app.services.teacher import check_teacher_is_taken, check_phone_is_taken

from typing import Optional, List

router = APIRouter()

@router.get("/teacher",
    response_model=TeacherList,
    name="profiles:get-profile",)
async def get_teachers(
    teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository)),
):
    teacher_list = await teacher_repo.search_teachers()
    data_object = []
    for item in teacher_list:
        teacher = TeacherInResponse(
            id=item["id"],
            name=item["username"],
            homeroomClassId=item["homeroom_class_id"],
            homeroomClass=item["class_name"],
            address=item["address"],
            phone=item["phone"]
        )
        data_object.append(teacher.dict(by_alias=True))
    return TeacherList(
        data=data_object
    )


@router.get("/teacher/unassigned",
    response_model=TeacherUnassignedList,
    name="profiles:get-teacher-unassigned-profile",)
async def get_teacher_unassigned(
    teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository)),
):
    teacher_list = await teacher_repo.search_teacher_unassigned()
    data_object = []

    for item in teacher_list:
        teacher = TeacherInResponseBase(
            value=item["value"],
            label=item["label"],
        )
        data_object.append(teacher)
    return TeacherUnassignedList(
        data=data_object
    )

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
        return JSONResponse({"errors":{"name":strings.TEACHER_EXITS}},400)

    if await check_phone_is_taken(teacher_repo, phone=teacher_create.phone) == True:
        # raise HTTPException(detail=strings.PHONE_EXITS, status_code=HTTP_400_BAD_REQUEST)
        return JSONResponse({"errors":{"phone":strings.PHONE_EXITS}},400)

    teacher_created = await teacher_repo.create_teacher(**teacher_create.dict())

    return TeacherInResponseCreate(
        name = teacher_created.name,
        phone = teacher_created.phone,
        # homeroom_class = teacher_created.homeroom_class,
        address = teacher_created.address
    )

@router.patch("/teacher/{teacher_id}")
async def update_teacher(teacher_id: int,
                        teacher_update: TeacherInCreate = Body(...,),
                        teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository))):
    # Check if the teacher exists
    teacher = await teacher_repo.get_teacher_by_id(teacher_id=teacher_id)

    if teacher is None:
       return JSONResponse({"error":strings.TEACHER_DO_NOT_EXITS},400)

    teacher_is_update = await teacher_repo.teacher_update(teacher_id=teacher_id,
                                                          name=teacher_update.name,
                                                          phone=teacher_update.phone,
                                                          address=teacher_update.address)

    return TeacherInResponseCreate(
        name = teacher_is_update.name,
        phone = teacher_is_update.phone,
        # homeroom_class = teacher_created.homeroom_class,
        address = teacher_is_update.address
    )

@router.delete("/teacher/{teacher_id}")
async def delete_teacher(teacher_id: int,
                        teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository))):
    # Check if the teacher exists
    teacher = await teacher_repo.get_teacher_by_id(teacher_id=teacher_id)
    if teacher is None:
       return JSONResponse({"error":strings.TEACHER_DO_NOT_EXITS},400)

    await teacher_repo.delete_teacher_by_id(teacher_id=teacher_id)

    return teacher_id

