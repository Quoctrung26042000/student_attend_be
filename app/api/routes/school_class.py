from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette import status
from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.school import ClassRepository
from app.db.repositories.teacher import TeacherRepository
from app.models.schemas.school import (
    ClassInfo,
    ClassInRepository,
    ClassInCreate,
    ClassDel,
    ClassRepositoryCreate
)
from app.resources import strings
from app.services import jwt
# from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.services.school import check_class_is_taken
from fastapi.responses import JSONResponse 
from fastapi.encoders import jsonable_encoder

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
    response_model=ClassRepositoryCreate,
    name="register:class",
)
async def register_class(
    class_create: ClassInCreate = Body(...),
    class_repo: ClassRepository = Depends(get_repository(ClassRepository)),
    teacher_repo: TeacherRepository = Depends(get_repository(TeacherRepository))
) -> ClassRepositoryCreate:
    
    missing_fields = [field for field, value in class_create.dict().items() if value is ""]
    error_msgs =[]
    if missing_fields:
        for field in missing_fields:
            error = {field:f"Phải nhập {field}"}
            error_msgs.append(error)
        return JSONResponse({"errors": error_msgs}, status_code=400)
    # Check if the teacher exists
    teacher = await teacher_repo.get_teacher_by_id(teacher_id=class_create.teacher_id)

    if teacher is None:
       JSONResponse({"errors":{"teacherId":strings.TEACHER_DO_NOT_EXITS}},400)
    
    
    if (await check_class_is_taken(class_repo, class_create.class_name)):
        return JSONResponse({"errors":{"className":strings.CLASS_TAKEN}},400)
 
    class_created = await class_repo.create_class(class_name=class_create.class_name,
                                                  grade_id=class_create.grade_id,
                                                  quantity=0)

    # Assi class for teacher_id
    teacher_update = await teacher_repo.update_class_id(teacher_id=class_create.teacher_id,class_id=class_created.id)

    return ClassRepositoryCreate(
            class_name=class_created.class_name,
            grade_id=class_created.grade_id,
            teacher_id=class_create.teacher_id
        )


@router.delete(
    "/class/{class_id}",
    name="Get:all-class",
)
async def delete_class_id(class_id:int,
                          class_repo: ClassRepository = Depends(get_repository(ClassRepository))):
    
    await class_repo.update_teacher_is_null(class_id=class_id)
    await class_repo.delete_class_id(class_id=class_id)

    return ClassDel(
        id=class_id
    )
