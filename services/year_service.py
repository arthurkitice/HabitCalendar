from database import get_db # Ajuste para o seu caminho real
from repositories import YearRepository
from dtos import YearDTO

class YearService:
    def get_year_by_id(self, year_id: int) -> YearDTO | None:
        with get_db() as db:
            year_repository = YearRepository(db)
            year = year_repository.get_year_by_id(year_id)
            if not year:
                return None
            return YearDTO.from_entity(year)

    def get_year_by_number(self, tracker_id: int, year_number: int) -> YearDTO | None:
        with get_db() as db:
            year_repository = YearRepository(db)
            year = year_repository.get_specific_year(tracker_id, year_number)
            if not year:
                return None
            return YearDTO.from_entity(year)

    def get_years_from_tracker(self, tracker_id: int) -> list[int]:
        with get_db() as db:
            year_repository = YearRepository(db)
            years = year_repository.get_years_from_tracker(tracker_id)
            if not years:
                return []
            return [y.number for y in years]

    def add_tracker_year(self, tracker_id: int, year_number: int) -> YearDTO | None:
        MIN_YEAR = 2000
        MAX_YEAR = 2100
        
        if not (MIN_YEAR <= year_number <= MAX_YEAR):
            return False

        with get_db() as db:
            year_repository = YearRepository(db)
            created_year = year_repository.create_year_with_cascade(tracker_id, year_number)
            if not created_year:
                return None
            return YearDTO.from_entity(created_year)
    
    def delete_year(self, tracker_id: int, year_number: int) -> bool:
        with get_db() as db:
            year_repository = YearRepository(db)
            return year_repository.delete_year(tracker_id, year_number)