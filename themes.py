from config import ThemeJSON
from dataclasses import dataclass

TEXT_COLOR = ( "#1F1F1F","#FFFFFF")
DEFAULT_COLOR = 'pink-man'

MAIN_COLORS = {
    "pink-man": {
        "fg": ("#FF6B9D", "#A82255"),
        "hover": ("#E85587", "#8E1644")
    },
    "red-dead": {
        "fg": ("#FA5B5B", "#BE1313"),
        "hover": ("#E04343", "#940707")
    },
    "radiance-orange": {
        "fg": ("#FF8C42", "#B85714"),
        "hover": ("#E6762D", "#96460F")
    },
    "golden-order": {
        "fg": ("#F7C948", "#B38A14"),
        "hover": ("#F5B92B", "#96730E")
    },
    "hierophant-green": {
        "fg": ("#4BB37A", "#1D7347"),
        "hover": ("#3A9D66", "#145936")
    },
    "authentic-cyan": {
        "fg": ("#34B3C1", "#0E9DAF"),
        "hover": ("#239BB0", "#0D5660")
    },
    "blue-prince": {
        "fg": ("#5C86E1", "#2459B8"),
        "hover": ("#4771CC", "#1B448C")
    },
    "purple-haze": {
        "fg": ("#9B70F8", "#4C1DB8"),
        "hover": ("#8554E3", "#381685")
    }
}

TRACKER_COLORS = {
    "Rosa": {
        "fg": ("#FF4D8C", "#D12163"),
        "hover": ("#E6407B", "#B01951")
    },
    "Vermelho": {
        "fg": ("#FF4757", "#D42031"),
        "hover": ("#E63E4D", "#B31725")
    },
    "Laranja": {
        "fg": ("#FF7722", "#D65A11"),
        "hover": ("#E66619", "#B3480B")
    },
    "Amarelo": {
        "fg": ("#FFD12A", "#D1A511"),
        "hover": ("#E6BA1E", "#B08A09")
    },
    "Verde": {
        "fg": ("#2ED169", "#17A34C"),
        "hover": ("#28B85C", "#138A40")
    },
    "Ciano": {
        "fg": ("#17C9EB", "#0E9AB8"),
        "hover": ("#13B1D1", "#0B8099")
    },
    "Azul": {
        "fg": ("#42A5F5", "#1E78D6"),
        "hover": ("#3893DE", "#1865B5")
    },
    "Roxo": {
        "fg": ("#B755F5", "#8021D1"),
        "hover": ("#A445E0", "#6A19B0")
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

@dataclass
class Theme:
    current_color: str
    palette: dict

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
            raise ValueError(f"Tema '{theme_name}' não encontrado")

PRIMARY_THEME = Theme(ThemeJSON.get_current_color(), MAIN_COLORS)
SECONDARY_THEME = Theme("default-theme", SECONDARY_COLORS)
TERTIARY_THEME = Theme("default-theme", TERTIARY_COLORS)

