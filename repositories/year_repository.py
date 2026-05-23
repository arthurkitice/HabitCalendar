import calendar
from sqlalchemy.orm import Session
from models import Year, Month, Day, Tracker
from constants import MONTHS

class YearRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_year_by_id(self, year_id: int) -> Year | None:
        return self.db.query(Year).filter(Year.id == year_id).first()

    def get_years_from_tracker(self, tracker_id: int):
        """Retorna todos os anos de um marcador, ordenados"""
        return self.db.query(Year).filter(Year.tracker_id == tracker_id).order_by(Year.number.asc()).all()

    def get_specific_year(self, tracker_id: int, year_number: int) -> Year | None:
        return self.db.query(Year).filter(Year.tracker_id == tracker_id, Year.number == year_number).first()

    def create_year_with_cascade(self, tracker_id: int, year_number: int) -> Year | None:
        if self.get_specific_year(tracker_id, year_number):
            return False 

        new_year = Year(number=year_number, tracker_id=tracker_id)

        for month_number, month_name in MONTHS.items():
            new_month = Month(name=month_name, number=month_number)
            
            days_in_month = calendar.monthrange(year_number, month_number)[1]
            for day_number in range(1, days_in_month + 1):
                new_month.days.append(Day(number=day_number, checked=False))
            
            new_year.months.append(new_month)

        self.db.add(new_year)
        
        self.db.commit()
        self.db.refresh(new_year)
        
        return new_year
    
    def delete_year(self, tracker_id: int, year_number: int) -> bool:
        year = self.get_specific_year(tracker_id, year_number)
        if not year:
            return False

        self.db.delete(year)
        self.db.commit()
        return True
    
    def get_all_checked_days(self, tracker_id: int, year: int) -> int:
        """Retorna a quantidade de dias marcados"""
        return self.db.query(Day)\
            .join(Month)\
            .join(Year)\
            .join(Tracker)\
            .filter(
                Tracker.id == tracker_id,
                Year.number == year,
                Day.checked == True
            ).count()