from app.db.errors import EntityDoesNotExist
from app.db.repositories.teacher import TeacherRepository


async def check_teacher_is_taken(repo: TeacherRepository , teacher_name: str) -> bool:
    try:
        teacher_row = await repo.get_teacher_by_name(teacher_name=teacher_name)
        print("teacher_row", teacher_row)
        if teacher_row is None :
            return False
        return True
    except EntityDoesNotExist:
        return False

async def check_phone_is_taken(repo: TeacherRepository , phone: str) -> bool:
    try:
        teacher_row = await repo.check_phone_is_taken(phone=phone)
        if teacher_row is None :
            return False
        return True
    except EntityDoesNotExist:
        return False


