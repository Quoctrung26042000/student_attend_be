from typing import Optional, List
from datetime import date
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository


class AttendanceRepository(BaseRepository):
    async def get_attend_infors(self, *, class_id: int) :
        attend_row = await queries.get_attend_infors(self.connection, class_id=class_id)
        return attend_row
    
    async def get_statistic(self) :
        attend_row = await queries.get_statistic(self.connection)
        return attend_row
    
    async def get_statistic_search(self,from_date, to_date):


        attend_row = await queries.get_statistic_search(self.connection,
                                                         from_date=from_date,
                                                         to_date=to_date)
        return attend_row
        
    async def search_statistic_detail(self,class_id,from_date, to_date):


        attend_row = await queries.search_statistic_detail(self.connection,
                                                            class_id=class_id,
                                                            from_date=from_date,
                                                            to_date=to_date)
        return attend_row
    
    async def search_attend_student_detail(self,student_id,from_date, to_date):


        attend_row = await queries.search_attend_student_detail(self.connection,
                                                                student_id=student_id,
                                                                from_date=from_date,
                                                                to_date=to_date)
        return attend_row
    
    async def update_attendance_student(self, *, student_update):

        attend_row = await queries.update_attendance_student(self.connection, student_update)
    
        return
    
    


    
    
    