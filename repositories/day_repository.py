from sqlalchemy.orm import Session
from models import Day, Month
from dtos import DayDTO

class DayRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_day_by_id(self, day_id: int):
        return self.db.query(Day).filter(Day.id == day_id).first()
    
    def get_day_number(self, day_id: int):
        return self.db.query(Day).filter(Day.id == day_id).first().number

    def create_day(self, number: int, checked: bool, month_id: int):
        new_day = Day(number=number, checked=checked, month_id=month_id)
        self.db.add(new_day)
        self.db.commit()
        self.db.refresh(new_day)
        
        return DayDTO(
            id=new_day.id, 
            number=new_day.number, 
            checked=new_day.checked, 
            month_id=new_day.month_id
        )
    
    def check_day(self, day_id: int):
        day = self.get_day_by_id(day_id)
        if day:
            day.checked = False if day.checked else True
            self.db.commit()
            self.db.refresh(day)
            return day
        return None