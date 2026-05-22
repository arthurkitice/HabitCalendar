from functools import wraps
import tkinter as tk
from .alter_tracker_view import AlterTrackerFrame
from .delete_tracker_view import DeleteTrackerView
from .delete_year_view import DeleteYearView
from .new_year_view import NewYearView
from .tracker_view import TrackerFrame
from .year_view import YearView
from .theme_view import ThemeView
from .settings_view import SettingsView

def apply_popup_binds(popup):
    """Gerencia uma pilha de popups para garantir que os atalhos afetem apenas o popup ativo."""
    root = popup.winfo_toplevel()
    
    # Configura os binds globais e a pilha apenas na primeira vez
    if not hasattr(root, "_popup_stack"):
        root._popup_stack = []
        
        def handle_enter(event):
            if root._popup_stack:
                top_popup = root._popup_stack[-1]
                # Se tiver 'save', salva. Se for popup de opção única, apenas fecha.
                if hasattr(top_popup, 'save'):
                    top_popup.save()
                else:
                    top_popup.destroy()
                    
        def handle_escape(event):
            if root._popup_stack:
                root._popup_stack[-1].destroy()
                
        root.bind('<Return>', handle_enter)
        root.bind('<Escape>', handle_escape)
        
    # Adiciona o popup atual no topo da pilha
    if popup not in root._popup_stack:
        root._popup_stack.append(popup)
    
    # Intercepta o fechamento para remover este popup da pilha e devolver o controle ao popup de baixo
    orig_destroy = popup.destroy
    def new_destroy():
        if popup in getattr(root, "_popup_stack", []):
            root._popup_stack.remove(popup)
        orig_destroy()
    popup.destroy = new_destroy

def _show_popup(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Cria a instância do popup
        popup = func(*args, **kwargs)
        
        # Aplica a nossa pilha de binds (a função que criamos na resposta anterior)
        apply_popup_binds(popup)

        # Exibe o popup
        popup.place(relx=0.5, rely=0.5, anchor="center")
        try:
            popup.wait_visibility()
        except tk.TclError:
            return
        
        popup.grab_set() # Trava a janela de baixo
        return popup
    return wrapper

@_show_popup
def alter_tracker_popup(parent, on_save, tracker_name=None, tracker_id=None):
    return AlterTrackerFrame(parent.winfo_toplevel(), on_save, tracker_name, tracker_id)

@_show_popup
def delete_tracker_popup(parent, on_save, tracker_name):
    """args -> on_save: callable, tracker_name: str"""
    return DeleteTrackerView(parent.winfo_toplevel(), on_save, tracker_name)

@_show_popup
def delete_year_popup(parent, on_save, year):
    return DeleteYearView(parent.winfo_toplevel(), on_save, year)

@_show_popup
def new_year_popup(parent, on_save, year):
    return NewYearView(parent.winfo_toplevel(), on_save, year)

@_show_popup
def tracker_popup(parent, tracker_name, tracker_id, on_year_remove):
    return TrackerFrame(parent.winfo_toplevel(), tracker_id, tracker_name, on_year_remove)

@_show_popup
def year_popup(parent, on_select, tracker_id, year, on_new_year):
    return YearView(parent.winfo_toplevel(), tracker_id, on_select, year, on_new_year)

@_show_popup
def theme_popup(parent, on_color_change, on_theme_change):
    return ThemeView(parent.winfo_toplevel(), on_color_change, on_theme_change)

@_show_popup
def settings_popup(parent, on_color_change, on_theme_change, on_language_change):
    return SettingsView(parent.winfo_toplevel(), on_color_change, on_theme_change, on_language_change)
