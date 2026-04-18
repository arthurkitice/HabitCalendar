from dataclasses import dataclass

@dataclass
class DayDTO:
    id: int
    number: int  # Usando string para facilitar a serialização
    checked: bool
    month_id: int
