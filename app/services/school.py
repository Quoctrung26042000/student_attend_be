from app.db.errors import EntityDoesNotExist
from app.db.repositories.school import (
     GradeRepository,
     ClassRepository
)
from app.db.repositories.account import AccountRepository


async def check_grade_is_taken(repo: GradeRepository , grade_name: int) -> bool:
    try:
        await repo.get_grade_by_username(grade_name=grade_name)
    except EntityDoesNotExist:
        return False
    return True


async def check_class_is_taken(repo: ClassRepository , class_name: str) -> bool:
    try:
        await repo.get_class_by_name(class_name=class_name)
    except EntityDoesNotExist:
        return False
    return True
