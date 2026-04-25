from pydantic import BaseModel
from models.tracker import Tracker
from .month_dto import MonthDTO

class TrackerDTO(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, tracker: Tracker) -> "TrackerDTO":
        return cls(id=tracker.id, name=tracker.name)

class TrackerWithMonthsDTO(BaseModel):
    id: int
    name: str
    months: list[MonthDTO]

    @classmethod
    def from_entity(cls, tracker: Tracker) -> "TrackerWithMonthsDTO":
        return cls(id=tracker.id, name=tracker.name, months=[MonthDTO.from_entity(m) for m in tracker.months])