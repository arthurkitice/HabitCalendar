from pydantic import BaseModel
from models.month import Month
from .day_dto import DayDTO

class MonthDTO(BaseModel):
    id: int
    name: str
    number: int
    
    @classmethod
    def from_entity(cls, month: Month) -> "MonthDTO":
        return cls(
            id=month.id,
            name=month.name,
            number=month.number
        )

class MonthWithDaysDTO(BaseModel):
    id: int
    name: str
    number: int
    days: list[DayDTO]
    
    @classmethod
    def from_entity(cls, month: Month) -> "MonthWithDaysDTO":
        return cls(
            id=month.id,
            name=month.name,
            number=month.number,
            days=[DayDTO.from_entity(d) for d in month.days]
        )