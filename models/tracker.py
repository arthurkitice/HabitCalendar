from dataclasses import dataclass
from .year import Year

@dataclass
class Tracker:
    id: int
    name: str

    @classmethod
    def from_row(cls, row) -> "Tracker":
        return cls(
            id=row["id"], 
            name=row["name"]
        )

@dataclass
class TrackerWithYears:
    id: int
    name: str
    years: list[Year]

    @classmethod
    def from_rows(cls, tracker_row, year_rows) -> "TrackerWithYears":
        return cls(
            id=tracker_row["id"], 
            name=tracker_row["name"],
            years=[Year.from_row(row) for row in year_rows]
        )