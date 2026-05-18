from enum import Enum, auto
from helper import carregar_icone_svg

STARTING_YEAR = 2026

MAIN_COLORS = {
    "hierophant-green (Default)": {
        "fg": ("#85C7A3", "#1A593D"), 
        "hover": ("#71B38F", "#14462F")
    },
    "blue-prince": {
        "fg": ("#8DA7DE", "#27488F"), 
        "hover": ("#7995CD", "#233C73")
    },
    "purple-haze": {
        "fg": ("#B398F5", "#4C1DB8"), 
        "hover": ("#9F82E6", "#381685")
    },
    "red-prince": {
        "fg": ("#ED8E8E", "#BE1313"), 
        "hover": ("#DB7A7A", "#940707")
    }
}

TRACKER_COLORS = {
    "Verde": {
        "fg": ("#7BC29A", "#2D634A"), 
        "hover": ("#6AB089", "#2A5A44")
    },
    "Azul": {
        "fg": ("#7BA1E2", "#344F87"), 
        "hover": ("#6A8DD1", "#31497E")
    },
    "Roxo": {
        "fg": ("#A891D9", "#7360A1"), 
        "hover": ("#957EC4", "#624F8E")
    },
    "Vermelho": {
        "fg": ("#D97B7B", "#A25353"), 
        "hover": ("#C76969", "#925050")
    },
    "Amarelo": {
        "fg": ("#D9C67A", "#A38F49"),
        "hover": ("#C7B368", "#938040")
    },
    "Laranja": {
        "fg": ("#D99A7A", "#9C6B4B"),
        "hover": ("#C78868", "#8C5E41")
    },
    "Rosa": {
        "fg": ("#D68EAD", "#9B637B"),
        "hover": ("#C47C9A", "#8B576D")
    },
    "Ciano": {
        "fg": ("#70C4CE", "#006B7B"),
        "hover": ("#61B0B9", "#3C6E75")
    }
}

SECONDARY_COLORS = {
    "default-theme": {
        "fg": ("#C5C5C5", "#303030"),
        "hover": ("#C0C0C0", "#272727")
    }
}

TERTIARY_COLORS = {
    "default-theme": {
        "fg": ("#8D8D8D", "#242424"),
        "hover": ("#707070", "#1E1E1E")
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

TEXT_COLOR = ( "#1F1F1F","#FFFFFF")

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
    LEFT_ARROW = carregar_icone_svg("left_arrow", (30, 30))
    RIGHT_ARROW = carregar_icone_svg("right_arrow", (30, 30))
    PLUS = carregar_icone_svg("plus", (30, 30))
    EDIT = carregar_icone_svg("pencil", (30, 30))
    TRASH = carregar_icone_svg("bin", (30, 30))
    CONFIG = carregar_icone_svg("settings", (30, 30))
    PALLETE = carregar_icone_svg("pallete", (20, 20))
    BIG_TRASH = carregar_icone_svg("bin", (40, 40))

ARROWS = {Direction.NEXT: IconImages.RIGHT_ARROW, Direction.PREV: IconImages.LEFT_ARROW}

ICONS = {
    IconType.EDIT: IconImages.EDIT,
    IconType.REMOVE: IconImages.TRASH,
    IconType.CONFIG: IconImages.CONFIG,
    IconType.PALLETE: IconImages.PALLETE,
    IconType.PLUS: IconImages.PLUS,
    IconType.BIG_TRASH: IconImages.BIG_TRASH
}