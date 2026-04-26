from enum import Enum, auto

STARTING_YEAR = 2026
MONTHS = {
    1: "Janeiro", 
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

class Direction(Enum):
    PREV = auto()
    NEXT = auto()

class Operation(Enum):
    CREATE = auto()
    EDIT = auto()