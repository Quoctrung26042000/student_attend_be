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
    AttendanceClass,
    AttendanceStatistics,
    AttendanceClassList,
    AttendanceStatisList
)
from app.resources import strings
from app.services import jwt

from typing import Optional, List

router = APIRouter()


@router.get(
    "/attendance/{class_id}",
    name="get:attendance",
)
async def get_atten(class_id:int,
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
) ->AttendanceClass :
    attend_infors =  await attend_repo.get_attend_infors(class_id=class_id)
    print("attenaaaaaaaaaaa", attend_infors)
    data_object = []
    if attend_infors:
        data_object = [AttendanceClass(**item) for item in attend_infors]

    return AttendanceClassList(data=data_object)


@router.get(
    "/statistics",
)
async def get_statistic(
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
) ->AttendanceStatisList :
    attend_infors =  await attend_repo.get_statistic()
    return AttendanceStatisList(data=attend_infors)



