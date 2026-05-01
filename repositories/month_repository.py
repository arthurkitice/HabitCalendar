from sqlalchemy.orm import Session
from models import Month

class MonthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_months(self):
        return self.db.query(Month).all()

    def get_month_by_id(self, month_id: int):
        return self.db.query(Month).filter(Month.id == month_id).first()
    
    def get_month_by_number(self, month_number: int):
        return self.db.query(Month).filter(Month.number == month_number).first()

    def get_month_by_year_number(self, tracker_id: int, year: int, month_number: int):
        return self.db.query(Month).filter(
            Month.tracker_id == tracker_id,\
            Month.year == year,\
            Month.number == month_number
            ).first()

    def get_years_from_tracker(self, tracker_id: int):
        return self.db.query(Month.year).filter(Month.tracker_id == tracker_id).distinct().order_by(Month.year).all()

    def create_month(self, name: str, number: int, year: int, tracker_id: int):
        month = Month(name=name, number=number, year=year, tracker_id=tracker_id)
        self.db.add(month)
        self.db.commit()
        self.db.refresh(month)
        
        return month