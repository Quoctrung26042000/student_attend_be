from typing import Optional, List

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.school import GradeInDB, ClassInDB


class GradeRepository(BaseRepository):
    async def create_grade(
        self,
        *,
        grade_name: int,
    ) -> GradeInDB:
        grade = GradeInDB(grade_name=grade_name)
        async with self.connection.transaction():
            grade_row = await queries.create_new_grade(
                self.connection,
                grade_name=grade.grade_name,
            )
        return grade.copy(update=dict(grade_row))
    
    async def get_grades(self) -> List[str] :
        grades_row = await queries.get_grades(self.connection)
        return grades_row
    
    async def get_grade_by_username(self, grade_name : str):
        grade_name = await queries.get_grade_by_username(self.connection, grade_name)

        if grade_name:
            return grade_name
        
        raise EntityDoesNotExist(
            "user with grade {0} does not exist".format(grade_name),
        )
    
    async def delete_grade_by_name(self, grade_name: int)-> None :
        await queries.delete_grade_by_name(self.connection, grade_name=grade_name)


class ClassRepository(BaseRepository):
    async def get_all_class(self) -> List[str] :
        class_row = await queries.get_all_class(self.connection)
        return class_row
    
    async def get_class_by_name(self, class_name: str):
        class_name = await queries.get_class_by_name(self.connection, class_name)
        if class_name:
            return class_name
        raise EntityDoesNotExist(
            "class with class_name {0} does not exist".format(class_name),
        )
    
    async def create_class(
        self,
        *,
        class_name: str,
        grade_id: int
    ) -> ClassInDB:
        class_created = ClassInDB(class_name=class_name, grade_id=grade_id)
        async with self.connection.transaction():
            class_row = await queries.create_new_class(
                self.connection,
                class_name=class_created.class_name,
                grade_id=class_created.grade_id,
            )
        return  class_created.copy(update=dict(class_row))
   