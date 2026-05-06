from sqlalchemy.orm import Session
from models import Day, Year, Month, Tracker

class DayRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_day_by_id(self, day_id: int):
        return self.db.query(Day).filter(Day.id == day_id).first()
    
    def get_day_number(self, day_id: int):
        return self.db.query(Day).filter(Day.id == day_id).first().number

    def check_day(self, day_id: int):
        day = self.get_day_by_id(day_id)
        day.checked = False if day.checked else True
        self.db.commit()
        self.db.refresh(day)
        
        return day
    
    def get_specific_day(self, tracker_id: int, year: int, month: int, day: int) -> Day | None:
        """Retorna um dia específico em um mês, ano e tracker"""
        return self.db.query(Day)\
            .join(Month)\
            .join(Year)\
            .join(Tracker)\
            .filter(
                Tracker.id == tracker_id,
                Year.number == year,
                Month.number == month,
                Day.number == day
            ).first()