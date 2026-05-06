from sqlalchemy.orm import Session
from models import Month, Year

class MonthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_months(self):
        return self.db.query(Month).all()

    def get_month_by_id(self, month_id: int):
        return self.db.query(Month).filter(Month.id == month_id).first()
    
    def get_month_by_year_number(self, tracker_id: int, year: int, month_number: int):
        return self.db.query(Month).join(Year).filter(
            Year.tracker_id == tracker_id,
            Year.number == year,
            Month.number == month_number
        ).first()
    