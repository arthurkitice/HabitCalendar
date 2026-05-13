from database import get_db
from repositories import MonthRepository
from dtos import MonthDTO, MonthWithDaysDTO

class MonthService:
    def get_all_months(self) -> list[MonthDTO] | None:
        with get_db() as db:
            month_repository = MonthRepository(db)
            months = month_repository.get_all_months()
            if not months:
                return None
            return [MonthDTO.from_entity(m) for m in months]
    
    def get_all_months_with_days(self) -> list[MonthWithDaysDTO] | None:
        with get_db() as db:
            month_repository = MonthRepository(db)
            months = month_repository.get_all_months()
            if not months:
                return None
            return [MonthWithDaysDTO.from_entity(m) for m in months]

    def get_month(self, month_id: int) -> MonthDTO | None:
        with get_db() as db:
            month_repository = MonthRepository(db)
            month = month_repository.get_month_by_id(month_id)
            if not month:
                return None
            return MonthDTO.from_entity(month)
    
    def get_month_with_days(self, month_id: int) -> MonthWithDaysDTO | None:
        with get_db() as db:
            month_repository = MonthRepository(db)
            month = month_repository.get_month_by_id(month_id)
            if not month:
                return None
            return MonthWithDaysDTO.from_entity(month)

    def get_specific_month(self, tracker_id: int, year: int, month_number: int) -> MonthDTO | None:
        with get_db() as db:
            month_repository = MonthRepository(db)
            month = month_repository.get_month_by_year_number(tracker_id, year, month_number)
            if not month:
                return None
            return MonthDTO.from_entity(month)
    
    def get_specific_month_with_days(self, tracker_id: int, year: int, month_number: int) -> MonthWithDaysDTO | None:
        with get_db() as db:
            month_repository = MonthRepository(db)
            month = month_repository.get_month_by_year_number(tracker_id, year, month_number)
            if not month:
                return None
            return MonthWithDaysDTO.from_entity(month)