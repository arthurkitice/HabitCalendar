from dataclasses import dataclass
from .month_dto import MonthDTO

@dataclass
class TrackerDTO:
    id: int
    name: str

@dataclass
class TrackerWithMonthsDTO:
    id: int
    name: str
    months: list[MonthDTO]