from app.db.errors import EntityDoesNotExist
from app.db.repositories.student import StudentRepository


async def check_student_is_taken(repo: StudentRepository , name: str) -> bool:
    try:
        student_row = await repo.get_student_by_name(name=name)
        print("student_rowstudent_rowstudent_row", student_row)
        if student_row is None :
            return False
        return True
    except EntityDoesNotExist:
        return False

async def check_phone_is_taken(repo: StudentRepository , phone: str) -> bool:
    try:
        student_row = await repo.get_student_by_phone(phone=phone)
        if student_row is None :
            return False
        return True
    except EntityDoesNotExist:
        return False


