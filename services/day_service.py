from database import get_connection
from repositories import DayRepository
from models import Day

class DayService:
    def get_day_by_id(self, day_id: int) -> Day | None:
        with get_connection() as conn:
            return DayRepository(conn).get_day_by_id(day_id)
    
    def get_day_number(self, day_id: int) -> Day | None:
        with get_connection() as conn:
            return DayRepository(conn).get_day_number(day_id)

    def check_day(self, day_id: int) -> Day | None:
        with get_connection() as conn:
            day_repository = DayRepository(conn)

            if not day_repository.get_day_by_id(day_id):
                return None
            
            day_repository.check_day(day_id)

            return day_repository.get_day_by_id(day_id)
    
    def get_specific_day(self, tracker_id: int, year: int, month: int, day: int) -> Day | None:
        with get_connection() as conn:
            return DayRepository(conn).get_specific_day(tracker_id, year, month, day)