import customtkinter as ctk
from themes import TEXT_COLOR
from ui.widgets import CustomButton
import tkinter as tk
import i18n

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
        self._remove_duplicates()

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
        print("teste")
        PopupFrame._popup_stack.remove(self)

        if len(PopupFrame._popup_stack):
            last_popup = PopupFrame._popup_stack[-1]
            last_popup.grab_set()
            last_popup.focus_set()
        else:
            top = self.winfo_toplevel()
            _toggle_background_cursors(top, hide=False)

        super().destroy()

    def _remove_duplicates(self):
        for popup in PopupFrame._popup_stack[:]:
            if type(popup) == type(self) and popup != self:
                popup.destroy()

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
            _set_silent_cursor(child, "arrow" if hide else "hand2")

        _toggle_background_cursors(child, hide)