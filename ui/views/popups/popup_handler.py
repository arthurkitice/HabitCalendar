from functools import wraps
from .alter_tracker_view import AlterTrackerFrame
from .delete_tracker_view import DeleteTrackerView
from .delete_year_view import DeleteYearView
from .new_year_view import NewYearView
from .tracker_view import TrackerFrame
from .year_view import YearView
from .theme_view import ThemeView

def _show_popup(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        parent = args[0] 
        root = parent.winfo_toplevel()

        if hasattr(root, "active_popup") and root.active_popup:
            try:
                root.active_popup.destroy()
            except:
                pass

        popup = func(*args, **kwargs)
        root.active_popup = popup

        popup.place(relx=0.5, rely=0.5, anchor="center")
        popup.wait_visibility()
        popup.grab_set()
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
def tracker_popup(parent, tracker_name, tracker_id):
    return TrackerFrame(parent.winfo_toplevel(), tracker_id, tracker_name)

@_show_popup
def year_popup(parent, on_select, tracker_id, year):
    return YearView(parent.winfo_toplevel(), tracker_id, on_select, year)

@_show_popup
def theme_popup(parent, on_color_change):
    return ThemeView(parent.winfo_toplevel(), on_color_change)

