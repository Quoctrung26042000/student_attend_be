from typing import Optional, List
from datetime import date
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.student import Student, StudentInDB


class StudentRepository(BaseRepository):
    async def get_student_by_id(self, *, id: int) :
        student_row = await queries.get_student_by_id(self.connection, id=id)
        return student_row
    
    async def get_student_by_name(self, *, name: str) :
        student_row = await queries.get_student_by_name(self.connection, name=name)
        return student_row
    
    async def get_student_by_phone(self, *, phone: str) :
        student_row = await queries.get_student_by_phone(self.connection, phone=phone)
        return student_row
    
    async def delete_student_by_id(self, *, id: int) :
        async with self.connection.transaction():
            student_row = await queries.delete_student_by_id(self.connection, id=id)
            
            await queries.update_quantity(self.connection,variable=-1,class_id=student_row["class_id"])

            await queries.delete_student_in_attendance(self.connection, student_id=id)

        return student_row
    
    async def get_all_student(self) :
        async with self.connection.transaction():
            student_row = await queries.get_all_student(self.connection)
        return student_row
    
    async def create_student(
        self,
        *,
        name: str,
        phone: str,
        gender: int,
        address: Optional[str],
        dateOfBirth:date,
        classId:int,
    ) -> StudentInDB:
        student = StudentInDB(name=name, phone=phone, address=address,
                            gender=gender, dateOfBirth=dateOfBirth,
                            classId=classId)
        async with self.connection.transaction():
            student_id = await queries.create_new_student(
                self.connection,
                name=student.name,
                phone=student.phone,
                gender=student.gender,
                address=student.address,
                date_of_birth=student.dateOfBirth,
                class_id=student.classId
            )
            await queries.update_quantity(self.connection,variable=1,class_id=classId)

            await queries.insert_new_student_in_attendance(self.connection, student_id=student_id)

        return student
    
    async def student_update(self, *,
                              id:int,
                              current_class_id:int,
                              object:dict) :
        student = StudentInDB(**object.dict())
        async with self.connection.transaction():
            student_row = await queries.student_update(
                self.connection,
                id=id,
                name=student.name,
                phone=student.phone,
                gender=student.gender,
                address=student.address,
                date_of_birth=student.dateOfBirth,
                class_id=student.classId,
            )
            if current_class_id != student.classId:
                # reduce the number of class 
                await queries.update_quantity(self.connection,variable=-1,class_id=current_class_id)
                
                # increasing the number
                await queries.update_quantity(self.connection,variable=1,class_id=student.classId)
        return student
    
  