import customtkinter as ctk
from constants import Direction, IconType, Icons

class _Day:
    FG_COLOR = "#333333" 
    HOVER_COLOR = "#282828"
    FG_COLOR_CHECKED = "#1A593D"
    HOVER_COLOR_CHECKED = "#14462F"
    FG_COLOR_DISABLED = "#2F2F2F"

class _Navigation:
    HOVER_COLOR = "#272727"

class _Sidebar:
    FG_COLOR = "#242424"
    HOVER_COLOR = "#1E1E1E"

class _Button:
    FG_COLOR = "#333333"
    HOVER_COLOR = "#272727"

def style_button(parent, text, command, **kwargs):
    button = ctk.CTkButton(
        parent,
        corner_radius=5,
        text=text,
        command=command,
        fg_color= _Button.FG_COLOR,
        hover_color= _Button.HOVER_COLOR,
        text_color="white",
        cursor="hand2"
    )
    button.configure(**kwargs)
    return button

class NavigationButton(ctk.CTkButton):
    def __init__(self, parent, direction, command, condition, height=50, width=65, **kwargs):
        self.direction = direction

        super().__init__(
            parent, 
            text="", 
            command=command,
            image=self._get_image(condition),
            fg_color="transparent",
            text_color="white",
            hover_color= _Navigation.HOVER_COLOR,
            cursor="hand2",
            height=height,
            width=width,
            **kwargs
        )
    
    def update_button(self, condition: bool, **kwargs):
        self.configure(image=self._get_image(condition), **kwargs)

    def _get_image(self, condition: bool):
        if condition:
            return Icons.PLUS
        return Icons.RIGHT_ARROW if self.direction == Direction.NEXT else Icons.LEFT_ARROW
    
class DayButton(ctk.CTkButton):
    def __init__(self, parent, day, command, checked, **kwargs):
        self.day = str(day)
        self.checked = checked
        configs = self._get_button_configs()

        super().__init__(
            parent, 
            corner_radius=20, 
            text=self.day, 
            command=command,
            text_color="white",
            text_color_disabled="gray",
            font=ctk.CTkFont(size=15, weight="bold"),
            **configs
        )
        self.configure(**kwargs)

    def _get_button_configs(self):
        return self._get_button_config() if self.day != "0" else self._get_disabled_button_config()

    def _get_disabled_button_config(self):
        return {
            "fg_color": _Day.FG_COLOR_DISABLED,
            "cursor": "arrow",
            "state": "disabled"
        }
    
    def _get_button_config(self):
        fg_color = _Day.FG_COLOR_CHECKED if self.checked else _Day.FG_COLOR
        hover_color = _Day.HOVER_COLOR_CHECKED if self.checked else _Day.HOVER_COLOR
        return {
            "fg_color": fg_color,
            "hover_color": hover_color,
            "cursor": "hand2",
            "state": "normal"
        }

    def update_button(self, day: int, command: callable, checked: bool, disabled: bool = False):
        self.day = str(day)
        self.configure(text=day)
        if not disabled:
            self.checked = checked
            configs = self._get_button_configs()
            self.configure(command=command, **configs)

    def check_day(self):
        self.checked = not self.checked
        fg_color = _Day.FG_COLOR_CHECKED if self.checked else _Day.FG_COLOR
        hover_color = _Day.HOVER_COLOR_CHECKED if self.checked else _Day.HOVER_COLOR
        self.configure(
            fg_color=fg_color,
            hover_color=hover_color
        )

class SidebarButton(ctk.CTkButton):
    def __init__(self, parent, command, icon_type: IconType | None = None, tracker: str | None = None, **kwargs):
        """
        Cria um botão da sidebar. IconTypes: IconType.EDIT, IconType.REMOVE e IconType.CONFIG (ainda não implementado)
        """
        self.icon_type = icon_type
        text = tracker or ""
        
        image = self._get_image()
        icon_width = {"width": 40} if self.icon_type else {}

        super().__init__(
            parent, 
            text=text,
            image=image,
            command=command,
            fg_color=_Sidebar.FG_COLOR,
            text_color="white",
            hover_color=_Sidebar.HOVER_COLOR,
            cursor="hand2",
            height=40,
            **icon_width
        )
        self.configure(**kwargs)

    def _get_image(self):
        match self.icon_type:
            case IconType.EDIT:
                return Icons.EDIT
            case IconType.REMOVE:
                return Icons.TRASH
            case _:
                return None