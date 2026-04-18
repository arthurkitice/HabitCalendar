from dataclasses import dataclass
from .day_dto import DayDTO

@dataclass
class MonthDTO:
    id: int
    name: str
    number: int

@dataclass
class MonthWithDaysDTO:
    id: int
    name: str
    number: int
    days: list[DayDTO]