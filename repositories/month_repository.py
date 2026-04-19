from sqlalchemy.orm import Session
from models import Month
from dtos import MonthDTO, DayDTO, MonthWithDaysDTO

class MonthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_months(self):
        months = self.db.query(Month).all()
        return [
            MonthDTO(
                id=month.id,
                name=month.name,
                number=month.number,
                year=month.year,
                tracker_id=month.tracker_id
            ) for month in months
        ]

    def get_month_by_id(self, month_id: int):
        month = self.db.query(Month).filter(Month.id == month_id).first()
        return MonthDTO(
            id=month.id,
            name=month.name,
            number=month.number,
            year=month.year,
            tracker_id=month.tracker_id
        ) if month else None
    
    def get_month_with_days_by_id(self, month_id: int):
        month = self.db.query(Month).filter(Month.id == month_id).first()
        if month:
            days = [
                DayDTO(
                    id=d.id, 
                    number=d.number,
                    checked=d.checked,
                    month_id=d.month_id
                ) 
                for d in month.day
            ]
            return MonthWithDaysDTO(
                id=month.id,
                name=month.name,
                number=month.number,
                year=month.year,
                tracker_id=month.tracker_id,
                days=days
            )
        return None
    
    def get_month_with_days_by_number(self, month_number: int):
        month = self.db.query(Month).filter(Month.number == month_number).first()
        if month:
            days = [
                DayDTO(
                    id=d.id, 
                    number=d.number,
                    checked=d.checked,
                    month_id=d.month_id
                ) 
                for d in month.day
            ]
            return MonthWithDaysDTO(
                id=month.id,
                name=month.name,
                number=month.number,
                year=month.year,
                tracker_id=month.tracker_id,
                days=days
            )
        return None
    
    def get_month_by_number(self, month_number: int):
        month = self.db.query(Month).filter(Month.number == month_number).first()
        return MonthDTO(
            id=month.id,
            name=month.name,
            number=month.number,
            year=month.year,
            tracker_id=month.tracker_id
        ) if month else None

    def create_month(self, name: str, number: int, year: int, tracker_id: int):
        new_month = Month(name=name, number=number, year=year, tracker_id=tracker_id)
        self.db.add(new_month)
        self.db.commit()
        self.db.refresh(new_month)
        
        return MonthDTO(
            id=new_month.id, 
            name=new_month.name, 
            number=new_month.number,
            year=new_month.year,
            tracker_id=new_month.tracker_id
        )
    
    def get_days_by_month_id(self, month_id: int):
        # Correção: Usar o método que retorna o DTO com os dias já mapeados
        month_with_days = self.get_month_with_days_by_id(month_id)
        if month_with_days:
            return month_with_days.days
        return None
    
    def get_days_by_month_number(self, month_number: int):
        month_with_days = self.get_month_with_days_by_number(month_number)
        if month_with_days:
            return month_with_days.days
        return None