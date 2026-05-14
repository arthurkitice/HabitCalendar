from enum import Enum, auto
from helper import carregar_icone_svg

STARTING_YEAR = 2026

MAIN_COLORS = {
    "hierophant-green (Default)": {
        "fg": "#1A593D", 
        "hover": "#14462F"
    },
    "blue-prince": {
        "fg": "#27488F", 
        "hover": "#233C73"
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

SECONDARY_COLORS = {
    "default-theme": {
        "fg": "#333333",
        "hover": "#272727"
    }
}

TERTIARY_COLORS = {
    "default-theme": {
        "fg": "#242424",
        "hover": "#1E1E1E"
    }
}

class Theme:
    def __init__(self, default_theme, palette_dict):
        self.current_color = default_theme
        self.palette = palette_dict

    def fg_color(self):
        return self.palette[self.current_color]["fg"]
    
    def hover_color(self):
        return self.palette[self.current_color]["hover"]
    
    def set_theme(self, theme_name):
        if theme_name in self.palette:
            self.current_color = theme_name
        else:
            print(f"Erro: Tema '{theme_name}' não encontrado!")

PRIMARY_THEME = Theme("hierophant-green (Default)", MAIN_COLORS)
SECONDARY_THEME = Theme("default-theme", SECONDARY_COLORS)
TERTIARY_THEME = Theme("default-theme", TERTIARY_COLORS)

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
    PALLETE = auto()
    PLUS = auto()
    BIG_TRASH = auto()

class IconImages:
    LEFT_ARROW = carregar_icone_svg("ui/icons/left_arrow_dark.svg", (30, 30))
    RIGHT_ARROW = carregar_icone_svg("ui/icons/right_arrow_dark.svg", (30, 30))
    PLUS = carregar_icone_svg("ui/icons/plus_dark.svg", (30, 30))
    EDIT = carregar_icone_svg("ui/icons/pencil_dark.svg", (30, 30))
    TRASH = carregar_icone_svg("ui/icons/bin_dark.svg", (30, 30))
    CONFIG = carregar_icone_svg("ui/icons/settings_dark.svg", (30, 30))
    PALLETE = carregar_icone_svg("ui/icons/pallete_dark.svg", (20, 20))
    BIG_TRASH = carregar_icone_svg("ui/icons/bin_dark.svg", (40, 40))

ARROWS = {Direction.NEXT: IconImages.RIGHT_ARROW, Direction.PREV: IconImages.LEFT_ARROW}

ICONS = {
    IconType.EDIT: IconImages.EDIT,
    IconType.REMOVE: IconImages.TRASH,
    IconType.CONFIG: IconImages.CONFIG,
    IconType.PALLETE: IconImages.PALLETE,
    IconType.PLUS: IconImages.PLUS,
    IconType.BIG_TRASH: IconImages.BIG_TRASH
}