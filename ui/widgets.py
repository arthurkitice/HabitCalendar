import customtkinter as ctk
from constants import IconType, ICONS, ARROWS, PRIMARY_THEME, SECONDARY_THEME, TERTIARY_THEME

FG_COLOR_DISABLED = "#2F2F2F"

class CustomButton(ctk.CTkButton):
    def __init__(self, parent, text, command, font_size = 20, bold = True, main_color = True, **kwargs):
        self.main_color = main_color
        fg_color = PRIMARY_THEME.fg_color() if self.main_color else SECONDARY_THEME.fg_color()
        hover_color = PRIMARY_THEME.hover_color() if self.main_color else SECONDARY_THEME.hover_color()

        super().__init__(
            parent,
            corner_radius=5,
            text=text,
            command=command,
            fg_color= fg_color,
            hover_color= hover_color,
            text_color="white",
            cursor="hand2",
            font=ctk.CTkFont(size=font_size, weight="bold" if bold else "normal")
        )
        self.configure(**kwargs)
        
    def reload_colors(self):
        if not self.main_color:
            return
        self.configure(fg_color=PRIMARY_THEME.fg_color(), hover_color=PRIMARY_THEME.hover_color())

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
            hover_color= SECONDARY_THEME.hover_color(),
            cursor="hand2",
            height=height,
            width=width,
            **kwargs
        )
        self.configure(**kwargs)
    
    def update_button(self, condition: bool, **kwargs):
        self.configure(image=self._get_image(condition), **kwargs)

    def _get_image(self, condition: bool):
        return ARROWS[self.direction] if not condition else ICONS[IconType.PLUS]
    
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
            "fg_color": FG_COLOR_DISABLED,
            "cursor": "arrow",
            "state": "disabled"
        }
    
    def _get_button_config(self):
        fg_color = PRIMARY_THEME.fg_color() if self.checked else SECONDARY_THEME.fg_color()
        hover_color = PRIMARY_THEME.hover_color() if self.checked else SECONDARY_THEME.hover_color()
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
        fg_color = PRIMARY_THEME.fg_color() if self.checked else SECONDARY_THEME.fg_color()
        hover_color = PRIMARY_THEME.hover_color() if self.checked else SECONDARY_THEME.hover_color()
        self.configure(
            fg_color=fg_color,
            hover_color=hover_color
        )

    def reload_colors(self):
        if not self.checked:
            return
        self.configure(fg_color=PRIMARY_THEME.fg_color(), hover_color=PRIMARY_THEME.hover_color())

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
            fg_color=TERTIARY_THEME.fg_color(),
            text_color="white",
            hover_color=TERTIARY_THEME.hover_color(),
            cursor="hand2",
            height=40,
            **icon_width
        )
        self.configure(**kwargs)

    def _get_image(self):
        return ICONS[self.icon_type] if self.icon_type else None
            
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
            fg_color=SECONDARY_THEME.fg_color(),
            text_color="white",
            hover_color=SECONDARY_THEME.hover_color(),
            cursor="hand2",
            height=40,
            width=40
        )
        self.configure(**kwargs)

    def _get_image(self):
        return ICONS[self.icon_type] if self.icon_type else None

class SmartScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, scroll_bar_on_right = True, **kwargs):
        super().__init__(master, **kwargs)

        if not scroll_bar_on_right:
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