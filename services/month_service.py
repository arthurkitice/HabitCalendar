from database import get_connection
from repositories import MonthRepository
from models import Month, MonthWithDays

class MonthService:
    def get_all_months(self) -> list[Month] | None:
        with get_connection() as conn:
            return MonthRepository(conn).get_all_months()

    def get_month(self, month_id: int) -> Month | None:
        with get_connection() as conn:
            return MonthRepository(conn).get_month_by_id(month_id)
    
    def get_month_with_days(self, month_id: int) -> MonthWithDays | None:
        with get_connection() as conn:
            return MonthRepository(conn).get_month_by_id(month_id)

    def get_specific_month(self, tracker_id: int, year: int, month_number: int) -> Month | None:
        with get_connection() as conn:
            return MonthRepository(conn).get_month_by_year_number(tracker_id, year, month_number)
        
    def get_specific_month_with_days(self, tracker_id: int, year: int, month_number: int) -> Month | None:
        with get_connection() as conn:
            month = MonthRepository(conn).get_month_by_year_number(tracker_id, year, month_number)
            return MonthRepository(conn).get_month_with_days_by_id(month.id) if month else None
        
    def get_checked_days_count(self, tracker_id: int, year: int, month: int) -> int | None:
        with get_connection() as conn:
            return MonthRepository(conn).get_all_checked_days(tracker_id, year, month)
        