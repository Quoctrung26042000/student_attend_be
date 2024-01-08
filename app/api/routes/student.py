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
    StudentInResponse,
    StudentList,
    StudentInUpdate
)
from app.db.repositories.account import Account
from app.resources import strings
from app.services import jwt
from app.services.student import check_student_is_taken, check_phone_is_taken
from app.api.dependencies.authentication import get_current_user_authorizer
from typing import Optional, List

router = APIRouter()

@router.get(
    "/student",
    name="get:student",
)
async def get_student(
    student_repo: StudentRepository = Depends(get_repository(StudentRepository)),
    current_teacher: Account = Depends(get_current_user_authorizer())
) :
    all_student =  await student_repo.get_all_student()

    if current_teacher.role == 2:
        all_student = [item for item in all_student if item['classId'] == current_teacher.classId]

    data_object = []
    # if all_student:
    #     data_object = [StudentInResponse(**item) for item in all_student]

    return {'data': all_student}

@router.post(
    "/student",
    status_code=HTTP_201_CREATED,
    name="register:student",
)
async def register_student(
    current_teacher: Account = Depends(get_current_user_authorizer()),
    student_create: StudentInUpdate = Body(...,),
    student_repo: StudentRepository = Depends(get_repository(StudentRepository)),
) -> StudentRepository:

    # if await check_student_is_taken(student_repo, name=student_create.name) == True:
    #     return JSONResponse({"errors":{"name":strings.STUDENT_EXITS}},400)
    
    if await check_phone_is_taken(student_repo, phone=student_create.phone) == True:
        return JSONResponse({"errors":{"phone":strings.PHONE_EXITS}},400)
    
    if current_teacher.role == 2:
        student_create.classId = current_teacher.classId
    
    student_created = await student_repo.create_student(**student_create.dict())
 
    return student_created

@router.delete(
    "/student/{student_id}",
    name="delete:student",
)
async def delete_student(student_id:int,
    student_repo: StudentRepository = Depends(get_repository(StudentRepository)),
):
    await student_repo.delete_student_by_id(id=student_id)

    return student_id

@router.patch(
    "/student/{student_id}",
    name="edit:student",
)
async def edit_student(student_id:int,
                       student_update: StudentInUpdate = Body(...,),
                       student_repo: StudentRepository = Depends(get_repository(StudentRepository)),
):
    # Current student 
    current_student = await student_repo.get_student_by_id(id=student_id)
    
    if current_student is None:
        return JSONResponse({"errors":strings.STUDENT_DO_NOT_EXITS},400)
    
    # if current_student['name'] != student_update.name:
    #     if await check_student_is_taken(student_repo, name=student_update.name) == True:
    #         return JSONResponse({"errors":{"name":strings.STUDENT_EXITS}},400)
        
    if current_student['phone'] != student_update.phone:
        if await check_phone_is_taken(student_repo, student_update.phone) == True:
            return JSONResponse({"errors":{"phone":strings.PHONE_EXITS}},400)

    current_class_id = current_student['class_id']
    student_is_update = await student_repo.student_update(id=student_id,
                                                          current_class_id=current_class_id,
                                                          object=student_update)

    return student_is_update


 




