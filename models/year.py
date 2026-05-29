from dataclasses import dataclass
from .month import Month

@dataclass
class Year:
    id: int
    number: int
    tracker_id: int

    @classmethod
    def from_row(cls, row) -> "Year":
        return cls(
            id=row["id"], 
            number=row["number"],
            tracker_id=row["tracker_id"]
        )

@dataclass
class YearWithMonths:
    id: int
    number: int
    tracker_id: int
    months: list[Month]

    @classmethod
    def from_rows(cls, year_row, month_rows) -> "Year":
        return cls(
            id=year_row["id"], 
            number=year_row["number"],
            tracker_id=year_row["tracker_id"],
            months=[Month.from_row(row) for row in month_rows]
        )