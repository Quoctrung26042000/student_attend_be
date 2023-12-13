from app.db.errors import EntityDoesNotExist
from app.db.repositories.teacher import TeacherRepository


async def check_teacher_is_taken(repo: TeacherRepository , teacher_name: str) -> bool:
    try:
        await repo.get_teacher_by_name(teacher_name=teacher_name)
    except EntityDoesNotExist:
        return False
    return True

async def check_phone_is_taken(repo: TeacherRepository , phone: str) -> bool:
    try:
        await repo.check_phone_is_taken(phone=phone)
    except EntityDoesNotExist:
        return False
    return True


