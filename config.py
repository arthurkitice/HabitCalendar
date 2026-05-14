import json
import os
from datetime import datetime

CONFIG_FILE = "app_settings.json"

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


class TrackerDateJSON:
    @staticmethod
    def save_current_date(tracker_id: int, month: int | None = None, year: int | None = None) -> None:
        data = _load_config_data()
        if month is None or year is None:
            month, year = 1, datetime.now().year
        data["trackers"][str(tracker_id)] = {"month": month, "year": year}
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
    def remove_tracker_date(tracker_id: int) -> bool:
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
    
class CurrentThemeJSON:
    @staticmethod
    def save_current_theme(theme: str) -> None:
        data = _load_config_data()
        data["config"]["current_theme"] = theme
        _save_config_data(data)

    @staticmethod
    def get_current_theme() -> str:
        data = _load_config_data()
        return data["config"].get("current_theme", "hierophant-green (Default)")