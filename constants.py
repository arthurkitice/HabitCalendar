from enum import Enum, auto
from helper import carregar_icone_svg

STARTING_YEAR = 2026

class AuxColorBlue:
    FG = "#27488F"
    HOVER = "#233C73"

class AuxColorGreen:
    FG = "#1A593D"
    HOVER = "#14462F"

class AuxColorGrey:
    FG = "#242424"
    HOVER = "#1E1E1E"

WEEK_DAYS = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

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

class IconType(Enum):
    EDIT = auto()
    REMOVE = auto()
    CONFIG = auto()
    BIG_TRASH = auto()

class Operation(Enum):
    CREATE = auto()
    EDIT = auto()

class Icons:
    LEFT_ARROW = carregar_icone_svg("ui/icons/left_arrow_dark.svg", (30, 30))
    RIGHT_ARROW = carregar_icone_svg("ui/icons/right_arrow_dark.svg", (30, 30))
    PLUS = carregar_icone_svg("ui/icons/plus_dark.svg", (30, 30))
    EDIT = carregar_icone_svg("ui/icons/pencil_dark.svg", (30, 30))
    TRASH = carregar_icone_svg("ui/icons/bin_dark.svg", (30, 30))
    CONFIG = carregar_icone_svg("ui/icons/settings_dark.svg", (30, 30))
    BIG_TRASH = carregar_icone_svg("ui/icons/bin_dark.svg", (40, 40))