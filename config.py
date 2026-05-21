import json
import os
from datetime import datetime
from database import APP_DIR

CONFIG_FILE = os.path.join(APP_DIR, "app_settings.json")

def _load_config_data() -> dict:
    default_data = {"config": {}, "trackers": {}}
    if not os.path.exists(CONFIG_FILE):
        return default_data
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            if "config" not in data: data["config"] = {}
            if "trackers" not in data: data["trackers"] = {}
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return default_data

def _save_config_data(data: dict) -> None:
    """Função auxiliar para centralizar o salvamento do JSON."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

class TrackerDataJSON:
    @staticmethod
    def save_current_date(tracker_id: int, month: int | None = None, year: int | None = None) -> None:
        data = _load_config_data()
        if month is None or year is None:
            month, year = 1, datetime.now().year

        tracker = data["trackers"].setdefault(str(tracker_id), {})

        tracker["month"] = month
        tracker["year"] = year
        _save_config_data(data)

    @staticmethod
    def get_last_month(tracker_id: int) -> int:
        data = _load_config_data()
        tracker_data = data["trackers"].get(str(tracker_id), {})
        if isinstance(tracker_data, int): return datetime.now().month
        return tracker_data.get("month", 1)

    @staticmethod
    def get_last_year(tracker_id: int) -> int:
        data = _load_config_data()
        tracker_data = data["trackers"].get(str(tracker_id), {})
        if isinstance(tracker_data, int): return datetime.now().year
        return tracker_data.get("year", datetime.now().year)
    
    @staticmethod
    def save_color(tracker_id: int, color: str) -> None:
        data = _load_config_data()
        data["trackers"][str(tracker_id)]["color"] = color
        _save_config_data(data)

    @staticmethod
    def get_color(tracker_id: int) -> int:
        data = _load_config_data()
        tracker_data = data["trackers"].get(str(tracker_id), {})
        if isinstance(tracker_data, int): return "Rosa"
        return tracker_data.get("color", "Rosa")

    @staticmethod
    def remove_tracker_data(tracker_id: int) -> bool:
        data = _load_config_data()
        tracker = data["trackers"].pop(str(tracker_id), None)
        
        if tracker is not None:
            _save_config_data(data)
            return True
        return False

class LastTrackerJSON:
    @staticmethod
    def save_current_tracker_id(tracker_id: int) -> None:
        data = _load_config_data()
        data["config"]["last_active_tracker"] = tracker_id
        _save_config_data(data)

    @staticmethod
    def get_last_tracker_id() -> int:
        data = _load_config_data()
        return data["config"].get("last_active_tracker", 0)

class SidebarStatusJSON:
    @staticmethod
    def save_sidebar_status(tracker_id: int) -> None:
        data = _load_config_data()
        data["config"]["sidebar_status"] = tracker_id
        _save_config_data(data)

    @staticmethod
    def get_sidebar_status() -> int:
        data = _load_config_data()
        return data["config"].get("sidebar_status", True)

class ThemeJSON:
    @staticmethod
    def save_current_color(color: str) -> None:
        data = _load_config_data()
        data["config"]["current_color"] = color
        _save_config_data(data)

    @staticmethod
    def save_current_theme(theme: str) -> None:
        data = _load_config_data()
        data["config"]["current_theme"] = theme
        _save_config_data(data)

    @staticmethod
    def save_current_language(language: str) -> None:
        data = _load_config_data()
        data["config"]["current_language"] = language
        _save_config_data(data)
    
    @staticmethod
    def toggle_new_year_popup_status() -> bool:
        data = _load_config_data()
        data["config"]["hide_new_year_popup"] = not ThemeJSON.is_new_year_popup_hidden()
        _save_config_data(data)

    @staticmethod
    def is_new_year_popup_hidden() -> bool:
        data = _load_config_data()
        return data["config"].get("hide_new_year_popup", False)

    @staticmethod
    def get_current_language() -> str:
        data = _load_config_data()
        return data["config"].get("current_language", None)

    @staticmethod
    def get_current_color() -> str:
        data = _load_config_data()
        return data["config"].get("current_color", "pink-man")

    @staticmethod
    def get_current_theme() -> str:
        data = _load_config_data()
        return data["config"].get("current_theme", "light")
    
class WindowSizeJSON:
    @staticmethod
    def unmaximize_window() -> bool:
        data = _load_config_data()
        data["config"]["window_maximized"] = False
        _save_config_data(data)

    @staticmethod
    def maximize_window() -> bool:
        data = _load_config_data()
        data["config"]["window_maximized"] = True
        _save_config_data(data)

    @staticmethod
    def save_window_size(width: int, height: int) -> bool:
        data = _load_config_data()
        data["config"]["window_width"] = width
        data["config"]["window_height"] = height
        _save_config_data(data)

    @staticmethod
    def is_window_maximized() -> bool:
        data = _load_config_data()
        return data["config"].get("window_maximized", False)

    @staticmethod
    def get_window_size() -> bool:
        data = _load_config_data()
        width = data["config"].get("window_width", 1100)
        height = data["config"].get("window_height", 700)
        return width, height