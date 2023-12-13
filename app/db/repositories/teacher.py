from typing import Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.teacher import Teacher, TeacherInDB


class TeacherRepository(BaseRepository):
    async def create_teacher(
        self,
        *,
        name: str,
        phone: str,
        homeroom_class: int,
    ) -> TeacherInDB:
        teacher = TeacherInDB(name=name, phone=phone, homeroom_class=homeroom_class)
        async with self.connection.transaction():
            teacher_row = await queries.create_new_teacher(
                self.connection,
                name=teacher.name,
                phone=teacher.phone,
                homeroom_class=teacher.homeroom_class,
            )
        return teacher.copy(update=dict(teacher_row))
    
    async def search_teachers(
        self,
    ) :
        async with self.connection.transaction():
            teachers = await queries.search_all_teacher(
                self.connection,
            )
        return teachers

    