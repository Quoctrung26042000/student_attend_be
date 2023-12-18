from typing import Optional, List
from datetime import date
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.student import Student, StudentInDB


class StudentRepository(BaseRepository):
    async def get_student_by_name(self, *, teacher_name: str) :
        teacher_row = await queries.get_teacher_by_name(self.connection, username=teacher_name)
        
        return teacher_row
    
    async def get_student_by_id(self, *, teacher_id: int) :
        teacher_row = await queries.get_teacher_by_id(self.connection, teacher_id=teacher_id)
        return teacher_row
    
    async def delete_teacher_by_id(self, *, teacher_id: int) :
        teacher_row = await queries.delete_teacher_by_id(self.connection, teacher_id=teacher_id)
        print("Teacher Row", teacher_row)
        return teacher_row
    
    async def create_student(
        self,
        *,
        name: str,
        phone: str,
        gender: int,
        address: Optional[str],
        date_of_birth:date,
        class_id:int,
    ) -> StudentInDB:
        student = StudentInDB(name=name, phone=phone, address=address,
                            gender=gender, date_of_birth=date_of_birth,
                            class_id=class_id)
        async with self.connection.transaction():
            student_row = await queries.create_new_student(
                self.connection,
                name=student.name,
                phone=student.phone,
                address=student.address
            )
        return student.copy(update=dict(student_row))
    
  