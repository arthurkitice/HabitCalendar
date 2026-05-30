import customtkinter as ctk
from icon_assets import PLUS
from themes import PRIMARY_THEME, SECONDARY_THEME, TERTIARY_THEME, TRACKER_COLORS, TEXT_COLOR
from config import TrackerDataJSON
import i18n
import tkinter as tk

class CustomButton(ctk.CTkButton):
    def __init__(
            self, 
            parent, 
            text=' ', 
            text_var=None, 
            command=None, 
            font_size = 20, 
            bold = True, 
            main_color = True, 
            **kwargs
        ):
        self.main_color = main_color
        fg_color = PRIMARY_THEME.fg_color() if self.main_color else SECONDARY_THEME.fg_color()
        hover_color = PRIMARY_THEME.hover_color() if self.main_color else SECONDARY_THEME.hover_color()

        super().__init__(
            parent,
            corner_radius=5,
            text=text,
            textvariable=text_var,
            command=command,
            fg_color= fg_color,
            hover_color= hover_color,
            text_color=TEXT_COLOR,
            cursor="hand2",
            font=ctk.CTkFont(size=font_size, weight="bold" if bold else "normal")
        )
        self.configure(**kwargs)
        
    def reload_colors(self):
        color1, color2 = PRIMARY_THEME.get_colors() if self.main_color else SECONDARY_THEME.get_colors()
        self.configure(fg_color=color1, hover_color=color2)

class NavigationButton(ctk.CTkButton):
    def __init__(self, parent, command, condition, icon, height=50, width=65, **kwargs):
        self.icon = icon

        super().__init__(
            parent, 
            text="", 
            command=command,
            image=self._get_image(condition),
            fg_color="transparent",
            text_color=TEXT_COLOR,
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
        return self.icon if not condition else PLUS
    
class DayButton(ctk.CTkButton):
    def __init__(self, parent, day, command, checked, tracker_id, **kwargs):
        self.day = str(day)
        self.checked = checked
        self.tracker_id = tracker_id
        self.color = TrackerDataJSON.get_color(self.tracker_id)

        self.check_colors = {
            "fg": TRACKER_COLORS[self.color]["fg"],
            "hover": TRACKER_COLORS[self.color]["hover"]
        }
        self.base_colors = {
            "fg": SECONDARY_THEME.fg_color(),
            "hover": SECONDARY_THEME.hover_color()
        }

        configs = self._get_button_configs()

        super().__init__(
            parent, 
            corner_radius=20, 
            text=self.day, 
            command=command,
            text_color=TEXT_COLOR,
            text_color_disabled="gray",
            font=ctk.CTkFont(size=15, weight="bold"),
            **configs
        )
        self.configure(**kwargs)

    def _get_button_configs(self):
        return self._get_button_config() if self.day != "0" else self._get_disabled_button_config()

    def _get_disabled_button_config(self):
        FG_COLOR_DISABLED = ("#D2D2D2", "#2F2F2F")
        return {
            "fg_color": FG_COLOR_DISABLED,
            "cursor": "arrow",
            "state": "disabled"
        }
    
    def _get_button_config(self):
        fg_color = self.check_colors["fg"] if self.checked else self.base_colors["fg"]
        hover_color = self.check_colors["hover"] if self.checked else self.base_colors["hover"]
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
        fg_color = self.check_colors["fg"] if self.checked else self.base_colors["fg"]
        hover_color = self.check_colors["hover"] if self.checked else self.base_colors["hover"]
        self.configure(
            fg_color=fg_color,
            hover_color=hover_color
        )

    def reload_colors(self):
        self.color = TrackerDataJSON.get_color(self.tracker_id)

        self.check_colors = {
            "fg": TRACKER_COLORS[self.color]["fg"],
            "hover": TRACKER_COLORS[self.color]["hover"]
        }
        if not self.checked:
            return
        self.configure(fg_color=self.check_colors["fg"], hover_color=self.check_colors["hover"])

class SidebarButton(ctk.CTkButton):
    def __init__(self, parent, command, icon = None, tracker: str | None = None, **kwargs):
        """
        Cria um botão da sidebar. IconTypes: IconType.EDIT, IconType.REMOVE e IconType.CONFIG
        """
        self.icon = icon
        text = tracker or ""
        
        text = text if len(text) < 15 else f"{text[:12]}..."

        icon_width = {"width": 40} if self.icon else {}

        super().__init__(
            parent, 
            text=text,
            image=icon,
            command=command,
            fg_color=TERTIARY_THEME.fg_color(),
            text_color=TEXT_COLOR,
            hover_color=TERTIARY_THEME.hover_color(),
            cursor="hand2",
            height=40,
            **icon_width
        )
        self.configure(**kwargs)

    def _get_image(self):
        return self.icon if self.icon else None
            
class IconButton(ctk.CTkButton):
    def __init__(self, parent, command, icon, text=None, text_var=None, **kwargs):
        """
        Cria um botão com ícone. IconTypes: IconType.EDIT, IconType.REMOVE e IconType.CONFIG
        """
        self.icon = icon
        
        image = self._get_image()

        if text_var is not None and text is None:
            text = " "
        elif text is None:
            text = ""

        super().__init__(
            parent,
            image=icon,
            text=text,
            textvariable=text_var,
            command=command,
            fg_color=SECONDARY_THEME.fg_color(),
            text_color=TEXT_COLOR,
            hover_color=SECONDARY_THEME.hover_color(),
            cursor="hand2",
            height=40,
            width=40
        )
        self.configure(**kwargs)

    def _get_image(self):
        return self.icon if self.icon else None
    
class SmartScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, scroll_bar_on_right=True, **kwargs):
        super().__init__(master, **kwargs)

        self._check_job = None
        self._scroll_on_right = scroll_bar_on_right
        
        # Captura a largura exata da barra de rolagem atual (geralmente 16) + 2px de respiro
        self._sb_width = self._scrollbar.cget("width") + 2

        # 1. Removemos do grid para evitar o loop de altura
        self._scrollbar.grid_forget()

        # 2. Canvas espalhado ocupando o espaço todo inicialmente
        self._parent_canvas.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self._parent_canvas.bind("<Configure>", self._check_scrollbar, add="+")
        self.bind("<Configure>", self._check_scrollbar, add="+") 
        
        self.bind_all("<MouseWheel>", self._force_mouse_scroll, add="+") 
        self.bind_all("<Button-4>", self._force_mouse_scroll, add="+")
        self.bind_all("<Button-5>", self._force_mouse_scroll, add="+")

    def _get_heights(self):
        bbox = self._parent_canvas.bbox("all") 
        content_height = (bbox[3] - bbox[1]) if bbox else 0
        visible_height = self._parent_canvas.winfo_height()
        return content_height, visible_height

    def _check_scrollbar(self, event=None):
        if self._check_job is not None:
            self.after_cancel(self._check_job)
        
        # REMOVIDO O DELAY EM MS!
        # after_idle executa o código instantaneamente assim que o motor 
        # gráfico tiver uma folga, impedindo lag sem precisar de cronômetro.
        self._check_job = self.after_idle(self._apply_scrollbar_logic)

    def _apply_scrollbar_logic(self):
        if not self.winfo_exists():
            return

        content_height, visible_height = self._get_heights()
        scrollbar_visivel = self._scrollbar.winfo_ismapped()

        if visible_height <= 1:
            # Opcional: Garante que ela comece limpa e escondida no frame 1
            if scrollbar_visivel:
                self._scrollbar.place_forget()
                self._parent_canvas.grid_configure(padx=0)
            return

        if content_height > visible_height:
            if scrollbar_visivel:
                return
            if self._scroll_on_right:
                self._scrollbar.place(relx=1.0, rely=0.0, relheight=1.0, anchor="ne")
                # Aplica padding dinâmico na direita, "empurrando" o conteúdo
                self._parent_canvas.grid_configure(padx=(0, self._sb_width))
            else:
                self._scrollbar.place(relx=0.0, rely=0.0, relheight=1.0, anchor="nw")
                # Aplica padding dinâmico na esquerda
                self._parent_canvas.grid_configure(padx=(self._sb_width, 0))
        elif scrollbar_visivel:
            self._scrollbar.place_forget()
            # Remove o padding quando a barra some, devolvendo a largura ao conteúdo
            self._parent_canvas.grid_configure(padx=0)

    def _force_mouse_scroll(self, event):
        if not self.winfo_exists():
            return

        # Verifica se não existe um popup segurando a tela
        if self.grab_current():
            return

        x, y = self.winfo_pointerxy()
        widget_under_mouse = self.winfo_containing(x, y)
        
        if widget_under_mouse and str(widget_under_mouse).startswith(str(self)):
            content_height, visible_height = self._get_heights()
            
            if content_height <= visible_height:
                return 

            if event.num == 4 or event.delta > 0:
                self._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self._parent_canvas.yview_scroll(1, "units")

class SliderButton(ctk.CTkFrame):
    def __init__(
            self, 
            parent, 
            values: list[str],
            command, 
            font_size = 20, 
            bold = True,
            width=200, 
            height=30,
            text_color=TEXT_COLOR,
            corner_radius=0,
            frame_fg_color=SECONDARY_THEME.fg_color(),
            frame_border_width=0,
            frame_border_color=TEXT_COLOR,
            button_corner_radius=5,
            button_fg_color=PRIMARY_THEME.fg_color(),
            button_hover_color=PRIMARY_THEME.hover_color(),
            button_border_width=0,
            button_border_color=TEXT_COLOR
        ):

        if not values:
            raise ValueError("values cannot be empty")

        self.command = command

        super().__init__(
            parent, 
            corner_radius=corner_radius, 
            width=width, 
            height=height,
            fg_color=frame_fg_color,
            border_width=frame_border_width,
            border_color=frame_border_color
        )
        
        self.grid_propagate(False)

        self.grid_columnconfigure((0, 2), weight=1, uniform='main')
        self.grid_columnconfigure(1, weight=3, uniform='main')
        self.grid_rowconfigure(0, weight=1)        

        self.values: list[str] = values
        self.current_index = 0

        font = ctk.CTkFont(size=font_size, weight='bold' if bold else 'normal')
        button_style = {
            "font": font,
            "fg_color": button_fg_color,
            "hover_color": button_hover_color,
            "text_color": text_color,
            "corner_radius": button_corner_radius,
            "border_width": button_border_width,
            "border_color": button_border_color
        }

        self.prev_btn = CustomButton(
            self,
            text='<', 
            command=self.prev_button, 
            **button_style
        )
        self.prev_btn.grid(row=0,column=0, padx=(0, 5), sticky="nsew")

        self.button = CustomButton(
            self, 
            command=self.on_click, 
            **button_style
        )
        self.button.grid(row=0,column=1, sticky="nsew")

        self.next_btn = CustomButton(
            self,
            text='>', 
            command=self.next_button, 
            **button_style
        )
        self.next_btn.grid(row=0,column=2, padx=(5, 0), sticky="nsew")

        self._update_value()

    def next_button(self):
        self.current_index = (self.current_index + 1) % len(self.values)
        self._update_value()
        
    def prev_button(self):
        self.current_index = (self.current_index - 1) % len(self.values)
        self._update_value()

    def on_click(self):
        if self.command: self.command(self.values[self.current_index])

    def get(self):
        return self.values[self.current_index]

    def set(self, value):
        if value in self.values:
            self.current_index = self.values.index(value)
            self._update_value()

    def _update_value(self):
        self.button.configure(text=self.values[self.current_index])

    def change_values(self, values: list[str]):
        self.values = values
        self.current_index = 0
        self._update_value()

    def reload_colors(self):
        color1, color2 = PRIMARY_THEME.get_colors()
        self.button.configure(fg_color=color1, hover_color=color2)
        self.next_btn.configure(fg_color=color1, hover_color=color2)
        self.prev_btn.configure(fg_color=color1, hover_color=color2)

class PopupFrame(ctk.CTkFrame):
    _popup_stack = []
    _binds_set = False

    def __init__(self, parent, on_confirm = None, main_col=0):
        super().__init__(
            parent, 
            width=500, 
            height=400,
            corner_radius=15,
            border_width=1, 
            border_color=TEXT_COLOR
        )

        PopupFrame._popup_stack.append(self)

        self.grid_propagate(False)

        self.on_confirm = on_confirm

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(main_col, weight=1)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=99, column=main_col, padx=10, pady=(0, 10), sticky="nsew")
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.after(0, self._display_popup)    
    
        self._setup_global_binds()

    def _display_popup(self):
        self.place(relx=0.5, rely=0.5, anchor="center")
        
        try:
            self.wait_visibility()
        except tk.TclError:
            pass

        self.grab_set()
        self.focus_set()

        if len(PopupFrame._popup_stack) == 1:
            top = self.winfo_toplevel()
            _toggle_background_cursors(top, hide=True)

    def _setup_global_binds(self):
        if not PopupFrame._binds_set:
            top_window = self.winfo_toplevel()
            top_window.bind('<Escape>', PopupFrame._global_handle_escape)
            top_window.bind('<Return>', PopupFrame._global_handle_enter)
            PopupFrame._binds_set = True
    
    @classmethod
    def _global_handle_escape(cls, event):
        """Encontra o popup do topo e o destrói"""
        if cls._popup_stack:
            cls._popup_stack[-1].destroy()

    @classmethod
    def _global_handle_enter(cls, event):
        """Encontra o popup do topo e tenta salvar"""
        if cls._popup_stack:
            topo = cls._popup_stack[-1]
            if hasattr(topo, 'save') and callable(topo.save):
                topo.save()
            else:
                topo.destroy()

    def build_back_button(self, text = None):
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.back_button = CustomButton(self.button_frame, text=text or i18n.t('actions.back'), command=self.destroy, font_size=15, height=35)
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def build_back_confirm_buttons(self, back_button_text = None, confirm_button_text = None):
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.confirm_button = CustomButton(self.button_frame, text=confirm_button_text or i18n.t('actions.confirm'), command=self.save, font_size=15, height=35)
        self.confirm_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.build_back_button(text = back_button_text)
        self.back_button.main_color = False
        self.back_button.reload_colors()

    def save(self):
        if self.on_confirm is not None:
            self.on_confirm()
        self.destroy()

    def destroy(self):
        PopupFrame._popup_stack.remove(self)

        if len(PopupFrame._popup_stack):
            last_popup = PopupFrame._popup_stack[-1]
            last_popup.grab_set()
            last_popup.focus_set()
        else:
            top = self.winfo_toplevel()
            _toggle_background_cursors(top, hide=False)

        super().destroy()

def _set_silent_cursor(ctk_widget, cursor_name):
    """Muda o cursor acessando as peças nativas do Tkinter, sem acordar o renderizador do CTK."""
    
    # Um CTkButton possui estes 3 componentes internos, que precisam ser alterados
    # individualmente para garantir que não haja falhas.
    # Isso é feito para evitar o "flick" dos botões ao atualizar o cursor.
    for attr in ['_canvas', '_text_label', '_image_label']:
        if hasattr(ctk_widget, attr):
            tk_subwidget = getattr(ctk_widget, attr)
            if tk_subwidget: # Garante que o elemento existe, pode ser que o botão não tenha imagem ou texto
                tk_subwidget.configure(cursor=cursor_name)

def _toggle_background_cursors(widget, hide=True):
    """Varre a tela inteira em milissegundos para esconder/devolver as mãozinhas do fundo."""
    for child in widget.winfo_children():
        if type(child).__name__ == "PopupFrame" or isinstance(child, PopupFrame):
            continue
            
        if isinstance(child, ctk.CTkButton):
            if hide:
                # Salva o cursor original
                if not hasattr(child, '_original_cursor'):
                    child._original_cursor = child.cget("cursor")
                
                _set_silent_cursor(child, "arrow")
            else:
                if hasattr(child, '_original_cursor'):
                    _set_silent_cursor(child, child._original_cursor)
                    del child._original_cursor
                    
        _toggle_background_cursors(child, hide)