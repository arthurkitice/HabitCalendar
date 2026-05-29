from database import get_connection
from repositories import YearRepository
from models import Year

class YearService:
    def get_year_by_id(self, year_id: int) -> Year | None:
        with get_connection() as conn:
            return YearRepository(conn).get_year_by_id(year_id)

    def get_year_by_number(self, tracker_id: int, year_number: int) -> Year | None:
        with get_connection() as conn:
            return YearRepository(conn).get_specific_year(tracker_id, year_number)

    def get_years_from_tracker(self, tracker_id: int) -> list[int]:
        with get_connection() as conn:
            years = YearRepository(conn).get_years_from_tracker(tracker_id)
            return [year.number for year in years]

    def add_tracker_year(self, tracker_id: int, year_number: int) -> Year | None:
        MIN_YEAR = 2000
        MAX_YEAR = 2100
        
        if not (MIN_YEAR <= year_number <= MAX_YEAR):
            return None

        with get_connection() as conn:
            return YearRepository(conn).create_year_with_cascade(tracker_id, year_number)
    
    def delete_year(self, tracker_id: int, year_number: int) -> bool:
        with get_connection() as conn:
            return YearRepository(conn).delete_year(tracker_id, year_number)
        
    def get_checked_days_count(self, tracker_id: int, year: int) -> int | None:
        with get_connection() as conn:
            return YearRepository(conn).get_all_checked_days(tracker_id, year)