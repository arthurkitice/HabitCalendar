from enum import Enum, auto
from helper import carregar_icone_svg

STARTING_YEAR = 2026

MAIN_COLORS = {
    "blue-prince": {
        "fg": "#27488F", 
        "hover": "#233C73"
    },
    "green-baby": {
        "fg": "#1A593D", 
        "hover": "#14462F"
    },
    "purple-haze": {
        "fg": "#4C1DB8", 
        "hover": "#381685"
    },
    "red-prince": {
        "fg": "#BE1313", 
        "hover": "#940707"
    }
}

class Theme:
    current = "green-baby"

    @classmethod
    def fg_color(cls):
        """Retorna a cor baseada no tema atual"""
        return MAIN_COLORS[cls.current]["fg"]
    
    @classmethod
    def hover_color(cls):
        """Retorna a cor baseada no tema atual"""
        return MAIN_COLORS[cls.current]["hover"]

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