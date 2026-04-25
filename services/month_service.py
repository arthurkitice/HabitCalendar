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

    def get_month_by_id(self, month_id: int) -> MonthDTO | None:
        month = self.month_repository.get_month_by_id(month_id)
        if not month:
            return None
        return MonthDTO.from_entity(month)
    
    def get_month_with_days_by_id(self, month_id: int) -> MonthWithDaysDTO | None:
        month = self.month_repository.get_month_by_id(month_id)
        if not month:
            return None
        return MonthWithDaysDTO.from_entity(month)
    
    def get_month_by_number(self, month_number: int) -> MonthDTO | None:
        """Retorna apenas o primeiro mês de acordo com o número"""
        month = self.month_repository.get_month_by_number(month_number)
        if not month:
            return None
        return MonthDTO.from_entity(month)

    def create_month(self, number: int, year: int, tracker_id: int) -> MonthDTO | None:
        tracker_repository = TrackerRepository(self.db)

        if not tracker_repository.get_tracker_by_id(tracker_id):
            return None

        month = self.month_repository.create_month(
            name=MONTHS[number], 
            number=number, 
            year=year, 
            tracker_id=tracker_id
        )

        return MonthDTO.from_entity(month)