from dataclasses import dataclass
from models.tracker import Tracker
from .year_dto import YearDTO

@dataclass
class TrackerDTO:
    id: int
    name: str

    @classmethod
    def from_entity(cls, tracker: Tracker) -> "TrackerDTO":
        return cls(id=tracker.id, name=tracker.name)

@dataclass
class TrackerWithYearsDTO:
    id: int
    name: str
    years: list[YearDTO]

    @classmethod
    def from_entity(cls, tracker: Tracker) -> "TrackerWithYearsDTO":
        return cls(id=tracker.id, name=tracker.name, years=[YearDTO.from_entity(m) for m in tracker.years])