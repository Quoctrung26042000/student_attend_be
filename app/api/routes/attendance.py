from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette import status
from fastapi.responses import JSONResponse  


from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.attendance import AttendanceRepository
from app.models.schemas.attendance import (
    AttendanceClass
)
from app.resources import strings
from app.services import jwt

from typing import Optional, List

router = APIRouter()


 
@router.get(
    "/attendance/{class_id}",
    name="get:attendance",
)
async def register_student(class_id:int,
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
) ->AttendanceClass :
    attend_infors =  await attend_repo.get_attend_infors(class_id=class_id)

    return attend_infors



