from pydantic import BaseModel
from models.day import Day

class DayDTO(BaseModel):
    id: int
    number: int
    checked: bool
    month_id: int
    
    @classmethod
    def from_entity(cls, day: Day) -> "DayDTO":
        return cls(
            id=day.id,
            number=day.number,
            checked=day.checked,
            month_id=day.month_id
        )