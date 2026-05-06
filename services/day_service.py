from sqlalchemy.orm import Session
from repositories import DayRepository, MonthRepository
from dtos import DayDTO

class DayService:
    def __init__(self, db: Session):
        self.db = db
        self.day_repository = DayRepository(self.db)

    def get_day_by_id(self, day_id: int) -> DayDTO | None:
        day = self.day_repository.get_day_by_id(day_id)
        if not day:
            return None
        return DayDTO.from_entity(day)
    
    def get_day_number(self, day_id: int) -> DayDTO | None:
        day = self.day_repository.get_day_number(day_id)
        if not day:
            return None
        return DayDTO.from_entity(day)

    def check_day(self, day_id: int) -> DayDTO | None:
        if not self.day_repository.get_day_by_id(day_id):
            return None
        day = self.day_repository.check_day(day_id)
        return DayDTO.from_entity(day)
    
    def get_specific_day(self, tracker_id: int, year: int, month: int, day: int) -> DayDTO | None:
        """Retorna um dia específico em um mês, ano e tracker"""
        return DayDTO.from_entity(self.day_repository.get_specific_day(tracker_id, year, month, day))
