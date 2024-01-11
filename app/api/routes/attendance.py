from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette import status
from fastapi.responses import JSONResponse  
from app.api.dependencies.authentication import get_current_user_authorizer

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.repositories.attendance import AttendanceRepository
from app.models.schemas.attendance import (
    AttendanceClass,
    AttendanceStatistics,
    AttendanceClassList,
    AttendanceStatisList,
    AttendanceStatisListV2,
    StatictInput,
    StudentInUpdate,
    AttendanceAproveAll
)
from app.db.repositories.account import Account
from app.models.domain.users import User
from app.resources import strings
from app.services import jwt

from typing import Optional, List
from fastapi import Query
from datetime import date, datetime

router = APIRouter()


@router.get(
    "/attendance/{class_id}",
    name="get:attendance",
)
async def get_atten(class_id:int,
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
) ->AttendanceClass :
    attend_infors =  await attend_repo.get_attend_infors(class_id=class_id)
    data_object = []
    if attend_infors:
        data_object = [AttendanceClass(**item) for item in attend_infors]

    return AttendanceClassList(data=data_object)


@router.get(
    "/statistics",
)
async def get_statistic(
    current_teacher: Account = Depends(get_current_user_authorizer()),
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
) ->AttendanceStatisListV2 :
    attend_infors =  await attend_repo.get_statistic()

    if current_teacher.role == 1:
        attend_infors = [item for item in attend_infors if item['classId'] == current_teacher.classId]
        
    return AttendanceStatisListV2(data=attend_infors)




@router.get("/search_statistic")
async def search_statistic(
    current_teacher: Account = Depends(get_current_user_authorizer()),
    from_date: str = Query(..., description="Start date"),
    to_date: str = Query(..., description="End date"),
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
) -> AttendanceStatisList:
    # Convert date strings to date objects with format "DD-MM-YYYY"
    from_date_parsed = datetime.strptime(from_date, "%d-%m-%Y").date()
    to_date_parsed = datetime.strptime(to_date, "%d-%m-%Y").date()


    attend_infors =  []

    attend_infors = await attend_repo.get_statistic_search(from_date=from_date_parsed,
                                                            to_date=to_date_parsed)
    
    if current_teacher.role == 1:
        attend_infors = [item for item in attend_infors if item['classId'] == current_teacher.classId]
        
    
    summary = {
        'total_students':sum(record['quantity'] for record in attend_infors) or 0,
        'total_classes':len(attend_infors) or 0,
        'total_absence_with_permission':sum(record['absenceWithPermission'] for record in attend_infors) or 0,
        'total_late':sum(record['late'] for record in attend_infors) or 0,
        'total_present':sum(record['present'] for record in attend_infors) or 0,
        'total_absence_without_permission':sum(record['absenceWithoutPermission'] for record in attend_infors) or 0,
    }

    if current_teacher.role == 1:
            summary['total_classes'] = attend_infors[0]['className'] if attend_infors else strings.TEACHER_UNASSIGNED

    
    return AttendanceStatisList(data=attend_infors,
                                summary=summary)


@router.get(
    "/attendance",
    name="get:attendance",
)
async def attendance(
    class_id:str = Query(..., description="Class id"),
    from_date: str = Query(..., description="Start date"),
    to_date: str = Query(..., description="End date"),
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
) ->AttendanceClass :
    # Convert date strings to date objects with format "DD-MM-YYYY"
    from_date_parsed = datetime.strptime(from_date, "%d-%m-%Y").date()
    to_date_parsed = datetime.strptime(to_date, "%d-%m-%Y").date()

    # 
    id = int(class_id)

    attend_infors =  await attend_repo.search_statistic_detail(class_id=id,
                                                               from_date=from_date_parsed,
                                                               to_date=to_date_parsed)
    response = {'data': attend_infors}
    return response


@router.get(
    "/attendance_student",
)
async def get_attend_student_detail(
    student_id:str = Query(..., description="Class id"),
    from_date: str = Query(..., description="Start date"),
    to_date: str = Query(..., description="End date"),
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
) ->AttendanceClass :
    # Convert date strings to date objects with format "DD-MM-YYYY"
    from_date_parsed = datetime.strptime(from_date, "%d-%m-%Y").date()
    to_date_parsed = datetime.strptime(to_date, "%d-%m-%Y").date()

    # 
    id = int(student_id)
    attend_infors = []
    response = {'data': attend_infors, 'nameStudent': ''} 


    attend_infors =  await attend_repo.search_attend_student_detail(student_id=id,
                                                                    from_date=from_date_parsed,
                                                                    to_date=to_date_parsed)
    
    print("attend_infors", attend_infors)

    if attend_infors:
        response['data'] = attend_infors
        response['nameStudent'] = attend_infors[0]['nameStudent']

    return response



@router.patch(
    "/attendance_update/{attendance_id}",
)
async def update_attendance_student(
    attendance_id:int,
    student_update : StudentInUpdate = Body(),
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
) ->AttendanceClass :

    update_row = await attend_repo.update_attendance_student(student_update=student_update,
                                                attendance_id=attendance_id)
    
    return update_row





@router.post(
    "/approve_all/{class_id}",
)
async def approve_all(
    class_id: int,
    attend_approve:AttendanceAproveAll = Body(),
    attend_repo: AttendanceRepository = Depends(get_repository(AttendanceRepository)),
):
    id = int(class_id)

    student_ids = await attend_repo.get_students_by_class_id(class_id=id)

    await attend_repo.approve_all_by_id(ids=student_ids, data_object=attend_approve)

    return {
        class_id:id
    }
                                                                   



