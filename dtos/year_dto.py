from dataclasses import dataclass
from models import Year
from .month_dto import MonthDTO

@dataclass
class YearDTO:
    id: int
    number: int

    @classmethod
    def from_entity(cls, year: Year) -> "YearDTO":
        return cls(id=year.id, number=year.number)

@dataclass
class YearWithMonthsDTO:
    id: int
    number: int
    months: list[MonthDTO]

    @classmethod
    def from_entity(cls, year: Year) -> "YearDTO":
        return cls(id=year.id, number=year.number, months=[MonthDTO.from_entity(m) for m in year.months])