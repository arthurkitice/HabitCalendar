from sqlalchemy.orm import Session
from repositories import MonthRepository, TrackerRepository
from dtos import MonthDTO, MonthWithDaysDTO
from constants import MONTHS

class MonthService:
    def __init__(self, db: Session):
        self.db = db
        self.month_repository = MonthRepository(self.db)

    def get_all_months(self) -> list[MonthDTO] | None:
        months = self.month_repository.get_all_months()
        if not months:
            return None
        return [MonthDTO.from_entity(m) for m in months]
    
    def get_all_months_with_days(self) -> list[MonthWithDaysDTO] | None:
        months = self.month_repository.get_all_months()
        if not months:
            return None
        return [MonthWithDaysDTO.from_entity(m) for m in months]

    def get_month(self, month_id: int) -> MonthDTO | None:
        month = self.month_repository.get_month_by_id(month_id)
        if not month:
            return None
        return MonthDTO.from_entity(month)
    
    def get_month_with_days(self, month_id: int) -> MonthWithDaysDTO | None:
        month = self.month_repository.get_month_by_id(month_id)
        if not month:
            return None
        return MonthWithDaysDTO.from_entity(month)

    def get_specific_month(self, tracker_id: int, year: int, month_number: int) -> MonthDTO | None:
        """Retorna um mês específico de acordo com o tracker, ano e número do mês"""
        month = self.month_repository.get_month_by_year_number(tracker_id, year, month_number)
        if not month:
            return None
        return MonthDTO.from_entity(month)
    
    def get_specific_month_with_days(self, tracker_id: int, year: int, month_number: int) -> MonthWithDaysDTO | None:
        """Retorna um mês específico com os dias de acordo com o tracker, ano e número do mês"""
        month = self.month_repository.get_month_by_year_number(tracker_id, year, month_number)
        if not month:
            return None
        return MonthWithDaysDTO.from_entity(month)