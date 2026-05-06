from pydantic import BaseModel
from models.tracker import Tracker
from .year_dto import YearDTO

class TrackerDTO(BaseModel):
    id: int
    name: str

    @classmethod
    def from_entity(cls, tracker: Tracker) -> "TrackerDTO":
        return cls(id=tracker.id, name=tracker.name)

class TrackerWithYearsDTO(BaseModel):
    id: int
    name: str
    years: list[YearDTO]

    @classmethod
    def from_entity(cls, tracker: Tracker) -> "TrackerWithYearsDTO":
        return cls(id=tracker.id, name=tracker.name, years=[YearDTO.from_entity(m) for m in tracker.years])