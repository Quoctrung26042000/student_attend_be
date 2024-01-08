from typing import Optional, List
from datetime import date
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository


class AttendanceRepository(BaseRepository):
    async def get_attend_infors(self, *, class_id: int) :
        attend_row = await queries.get_attend_infors(self.connection, class_id=class_id)
        print("aaaaaaaaaaaaaa",attend_row)
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
    
    async def update_attendance_student(self, *, student_update, attendance_id):

        attend_row = await queries.update_attendance_student(self.connection,
                                                              attendance_id=attendance_id,
                                                              status=student_update.status,
                                                              note=student_update.note)
        return attend_row
    
    async def approve_all_by_id(self, *, ids, data_object):

        attend_row = await queries.approve_all_by_id(self.connection,
                                                              ids=ids,
                                                              status=data_object.status,
                                                              note=data_object.note)
        return attend_row
    

    async def get_students_by_class_id(self, *, class_id):

        ids = await queries.get_students_by_class_id(self.connection,
                                                     class_id=class_id)
        return ids
    
    


    
    
    