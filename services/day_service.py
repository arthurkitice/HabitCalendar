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

    def create_day(self, number: int, checked: bool, month_id: int) -> DayDTO | None:
        month_repository = MonthRepository(self.db)

        if not month_repository.get_month_by_id(month_id):
            return None

        day = self.day_repository.create_day(
            number=number,
            checked=checked,
            month_id=month_id
        )

        return DayDTO.from_entity(day)
    
    def check_day(self, day_id: int) -> DayDTO | None:
        if not self.day_repository.get_day_by_id(day_id):
            return None
        day = self.day_repository.check_day(day_id)
        return DayDTO.from_entity(day)
        
