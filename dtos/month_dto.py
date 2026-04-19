from dataclasses import dataclass
from .day_dto import DayDTO

@dataclass
class MonthDTO:
    id: int
    name: str
    number: int
    year: int
    tracker_id: int

@dataclass
class MonthWithDaysDTO:
    id: int
    name: str
    number: int
    year: int
    tracker_id: int
    days: list[DayDTO]