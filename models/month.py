from dataclasses import dataclass
from .day import Day

@dataclass
class Month:
    id: int
    number: int
    year_id: int
    
    @classmethod
    def from_row(cls, row) -> "Month":
        return cls(
            id=row["id"],
            number=row["number"],
            year_id=row["year_id"]
        )

@dataclass
class MonthWithDays:
    id: int
    number: int
    year_id: int
    days: list[Day]
    
    @classmethod
    def from_rows(cls, month_row, day_rows) -> "MonthWithDays":
        return cls(
            id=month_row["id"],
            number=month_row["number"],
            year_id=month_row["year_id"],
            days=[Day.from_row(row) for row in day_rows]
        )