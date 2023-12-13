from typing import Optional, List

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.teacher import Teacher, TeacherInDB


class TeacherRepository(BaseRepository):
    async def get_teacher_by_name(self, *, teacher_name: str) :
        teacher_row = await queries.get_teacher_by_name(self.connection, username=teacher_name)
        if teacher_row:
            return teacher_row
        raise EntityDoesNotExist("teacher_row with username {0} does not exist".format(teacher_row))
    
    async def check_phone_is_taken(self, *, phone: str) :
        teacher_row = await queries.check_phone_is_taken(self.connection, phone=phone)
        if teacher_row:
            return teacher_row
        raise EntityDoesNotExist("teacher with phone {0} does not exist".format(teacher_row))
    
    async def create_teacher(
        self,
        *,
        name: str,
        phone: str,
        address: Optional[str]
    ) -> TeacherInDB:
        teacher = TeacherInDB(name=name, phone=phone, address=address)
        async with self.connection.transaction():
            teacher_row = await queries.create_new_teacher(
                self.connection,
                name=teacher.name,
                phone=teacher.phone,
                address=teacher.address
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
    
    async def search_teacher_unassigned(
        self,
    ) :
        async with self.connection.transaction():
            teachers = await queries.search_teacher_unassigned(
                self.connection,
            )
        return teachers
    
    

    