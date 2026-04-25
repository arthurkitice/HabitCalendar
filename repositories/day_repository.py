from sqlalchemy.orm import Session
from models import Day

class DayRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_day_by_id(self, day_id: int):
        return self.db.query(Day).filter(Day.id == day_id).first()
    
    def get_day_number(self, day_id: int):
        return self.db.query(Day).filter(Day.id == day_id).first().number

    def create_day(self, number: int, checked: bool, month_id: int):
        day = Day(number=number, checked=checked, month_id=month_id)
        self.db.add(day)
        self.db.commit()
        self.db.refresh(day)
        
        return day
    
    def check_day(self, day_id: int):
        day = self.get_day_by_id(day_id)
        day.checked = False if day.checked else True
        self.db.commit()
        self.db.refresh(day)
        
        return day
