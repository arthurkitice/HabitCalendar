from enum import Enum, auto
from helper import carregar_icone_svg

STARTING_YEAR = 2026

MAIN_COLORS = {
    "hierophant-green": {
        "fg": ("#4BB37A", "#1D7347"),
        "hover": ("#3A9D66", "#145936")
    },
    "blue-prince": {
        "fg": ("#5C86E1", "#2459B8"),
        "hover": ("#4771CC", "#1B448C")
    },
    "purple-haze": {
        "fg": ("#9B70F8", "#4C1DB8"),
        "hover": ("#8554E3", "#381685")
    },
    "red-dead": {
        "fg": ("#FA5B5B", "#BE1313"),
        "hover": ("#E04343", "#940707")
    },
    "pinkman": {
        "fg": ("#FF6B9D", "#A82255"),
        "hover": ("#E85587", "#8E1644")
    },
    "golden-order": {
        "fg": ("#F7C948", "#B38A14"),
        "hover": ("#F5B92B", "#96730E")
    },
    "radiance-orange": {
        "fg": ("#FF8C42", "#B85714"),
        "hover": ("#E6762D", "#96460F")
    },
    "authentic-cyan": {
        "fg": ("#34B3C1", "#0E9DAF"),
        "hover": ("#239BB0", "#0D5660")
    }
}

TRACKER_COLORS = {
    "Verde": {
        "fg": ("#2ED169", "#17A34C"),
        "hover": ("#28B85C", "#138A40")
    },
    "Azul": {
        "fg": ("#42A5F5", "#1E78D6"),
        "hover": ("#3893DE", "#1865B5")
    },
    "Roxo": {
        "fg": ("#B755F5", "#8021D1"),
        "hover": ("#A445E0", "#6A19B0")
    },
    "Vermelho": {
        "fg": ("#FF4757", "#D42031"),
        "hover": ("#E63E4D", "#B31725")
    },
    "Amarelo": {
        "fg": ("#FFD12A", "#D1A511"),
        "hover": ("#E6BA1E", "#B08A09")
    },
    "Laranja": {
        "fg": ("#FF7722", "#D65A11"),
        "hover": ("#E66619", "#B3480B")
    },
    "Rosa": {
        "fg": ("#FF4D8C", "#D12163"),
        "hover": ("#E6407B", "#B01951")
    },
    "Ciano": {
        "fg": ("#17C9EB", "#0E9AB8"),
        "hover": ("#13B1D1", "#0B8099")
    }
}

SECONDARY_COLORS = {
    "default-theme": {
        "fg": ("#E4E4E4", "#303030"),
        "hover": ("#D1D1D1", "#272727")
    }
}

TERTIARY_COLORS = {
    "default-theme": {
        "fg": ("#E8E8E8", "#242424"),
        "hover": ("#D2D2D2", "#1E1E1E")
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
    
    def get_colors(self):
        return self.fg_color(), self.hover_color()
    
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

LANGUAGES = {
    "en": "English",
    "es": "Español",
    "pt": "Português",
    "it": "Italiano",
    "fr": "Français",
    "el": "Ελληνικά",
    "ru": "Русский",
    "zh": "中文",
    "ko": "한국어"
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