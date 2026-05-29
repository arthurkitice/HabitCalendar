from dataclasses import dataclass

@dataclass
class Day:
    id: int
    number: int
    checked: bool
    month_id: int
    
    @classmethod
    def from_row(cls, row) -> "Day":
        return cls(
            id=row["id"],
            number=row["number"],
            checked=bool(row["checked"]),
            month_id=row["month_id"]
        )