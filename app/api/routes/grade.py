from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette import status
from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.school import GradeRepository
from app.models.schemas.school import (
    GradeInCreate,
    GradeInRepository,
    GradeInfo,
    GradeInDB
)
from app.resources import strings
from app.services import jwt
# from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.services.school import check_grade_is_taken

router = APIRouter()


@router.post(
    "/grade",
    status_code=HTTP_201_CREATED,
    response_model=GradeInRepository,
    name="register:grade",
)
async def register_grade(
    grade_create: GradeInCreate = Body(),
    grade_repo: GradeRepository = Depends(get_repository(GradeRepository)),
) -> GradeInRepository:
    
    if await check_grade_is_taken(grade_repo, grade_create.grade_name):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.GRADE_TAKEN,
        )
    grade_created = await grade_repo.create_grade(**grade_create.dict())
    
    return GradeInRepository(
        grade_name = grade_created.grade_name
    )

@router.get(
    "/grade",
    response_model=GradeInfo,
    name="Get:grades",
)
async def get_grades(grade_repo: GradeRepository = Depends(get_repository(GradeRepository))):
    grades = await grade_repo.get_grades()
    return GradeInfo(
        data=grades
    )

@router.delete(
    "/grade/{grade_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="comments:delete-grade",
    response_class=Response,  
)
async def delete_grade(grade_name: int,
    grade_repo: GradeRepository = Depends(get_repository(GradeRepository)),
) -> None:
    if (await check_grade_is_taken(grade_repo, grade_name)) == False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=strings.GRADE_DOES_NOT_EXIST,
        )
    return await grade_repo.delete_grade_by_name(grade_name)



