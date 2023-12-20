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
    
    
    