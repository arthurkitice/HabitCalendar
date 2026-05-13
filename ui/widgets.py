import customtkinter as ctk
from constants import Direction, IconType, Icons, AuxColorGreen
import tkinter as tk

class _Day:
    FG_COLOR = "#333333" 
    HOVER_COLOR = "#282828"
    FG_COLOR_CHECKED = AuxColorGreen.FG
    HOVER_COLOR_CHECKED = AuxColorGreen.HOVER
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
        Cria um botão da sidebar. IconTypes: IconType.EDIT, IconType.REMOVE e IconType.CONFIG
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
            case IconType.CONFIG:
                return Icons.CONFIG
            case _:
                return None
            
class IconButton(ctk.CTkButton):
    def __init__(self, parent, command, icon_type: IconType, **kwargs):
        """
        Cria um botão com ícone. IconTypes: IconType.EDIT, IconType.REMOVE e IconType.CONFIG
        """
        self.icon_type = icon_type
        
        image = self._get_image()

        super().__init__(
            parent,
            image=image,
            text="",
            command=command,
            fg_color=_Sidebar.FG_COLOR,
            text_color="white",
            hover_color=_Sidebar.HOVER_COLOR,
            cursor="hand2",
            height=40,
            width=40
        )
        self.configure(**kwargs)

    def _get_image(self):
        match self.icon_type:
            case IconType.EDIT:
                return Icons.EDIT
            case IconType.REMOVE:
                return Icons.TRASH
            case IconType.CONFIG:
                return Icons.CONFIG
            case IconType.BIG_TRASH:
                return Icons.BIG_TRASH
            case _:
                return None
            
import customtkinter as ctk

class SmartScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._parent_frame.grid_columnconfigure(0, weight=0)
        self._parent_frame.grid_columnconfigure(1, weight=1)

        self._scrollbar.grid(row=1, column=0, sticky="ns", padx=(5, 0))
        self._parent_canvas.grid(row=1, column=1, sticky="nsew")

        # Monitora mudanças de tamanho direto no Canvas (a tela de rolagem)
        self._parent_canvas.bind("<Configure>", self._check_scrollbar, add="+")
        
        # O add="+" garante que não vamos sobrescrever outros eventos do sistema
        self.bind_all("<MouseWheel>", self._force_mouse_scroll, add="+") 
        self.bind_all("<Button-4>", self._force_mouse_scroll, add="+")
        self.bind_all("<Button-5>", self._force_mouse_scroll, add="+")

    def _get_heights(self):
        """Calcula a altura real do conteúdo e a altura visível na tela."""
        self._parent_canvas.update_idletasks()
        
        # bbox("all") retorna (x_inicial, y_inicial, x_final, y_final) de todos os itens
        bbox = self._parent_canvas.bbox("all") 
        
        # Se tiver itens, a altura é y_final - y_inicial. Se estiver vazio, é 0.
        content_height = (bbox[3] - bbox[1]) if bbox else 0
        visible_height = self._parent_canvas.winfo_height()
        
        return content_height, visible_height

    def _check_scrollbar(self, event=None):
        content_height, visible_height = self._get_heights()

        # Agora a matemática funciona perfeitamente!
        if content_height > visible_height:
            self._scrollbar.grid()
        else:
            self._scrollbar.grid_remove()

    def _force_mouse_scroll(self, event):
        if not self.winfo_exists():
            return

        # 1. Checa se o mouse está realmente em cima deste frame de rolagem
        x, y = self.winfo_pointerxy()
        widget_under_mouse = self.winfo_containing(x, y)
        
        if widget_under_mouse and str(widget_under_mouse).startswith(str(self)):
            
            # 2. A MÁGICA CONTRA O "SCROLL NO VAZIO" ACONTECE AQUI:
            content_height, visible_height = self._get_heights()
            if content_height <= visible_height:
                return # Interrompe a função. O scroll não faz nada!

            # 3. Se passou pela verificação acima, permite rolar a tela
            if event.num == 4 or event.delta > 0:
                self._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self._parent_canvas.yview_scroll(1, "units")