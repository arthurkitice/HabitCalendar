from pydantic import BaseModel
from models.month import Month
from .day_dto import DayDTO

class MonthDTO(BaseModel):
    id: int
    name: str
    number: int
    year: int
    tracker_id: int
    
    @classmethod
    def from_entity(cls, month: Month) -> "MonthDTO":
        return cls(
            id=month.id,
            name=month.name,
            number=month.number,
            year=month.year,
            tracker_id=month.tracker_id
        )

class MonthWithDaysDTO(BaseModel):
    id: int
    name: str
    number: int
    year: int
    tracker_id: int
    days: list[DayDTO]
    
    @classmethod
    def from_entity(cls, month: Month) -> "MonthWithDaysDTO":
        return cls(
            id=month.id,
            name=month.name,
            number=month.number,
            year=month.year,
            tracker_id=month.tracker_id,
            days=[DayDTO.from_entity(d) for d in month.days]
        )