import json
import os
from datetime import datetime

CONFIG_FILE = "app_settings.json"

def get_last_month(tracker_id: int) -> int:
    if not os.path.exists(CONFIG_FILE):
        return datetime.now().month
    
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            tracker_data = data.get(str(tracker_id), {})
            
            # Se for int (legado da sua versão anterior com index), ignora
            if isinstance(tracker_data, int): 
                return datetime.now().month
                
            return tracker_data.get("month", datetime.now().month)
    except (json.JSONDecodeError, FileNotFoundError):
        return datetime.now().month

def get_last_year(tracker_id: int) -> int:
    if not os.path.exists(CONFIG_FILE):
        return datetime.now().year
    
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            tracker_data = data.get(str(tracker_id), {})
            
            # Se for int (legado), ignora
            if isinstance(tracker_data, int): 
                return datetime.now().year
                
            return tracker_data.get("year", datetime.now().year)
    except (json.JSONDecodeError, FileNotFoundError):
        return datetime.now().year

def save_current_date(tracker_id: int, month: int, year: int) -> None:
    data = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass 
    
    # Cria a chave aninhada com o ID do tracker
    data[str(tracker_id)] = {"month": month, "year": year}
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def save_current_tracker_id(tracker_id: int) -> None:
    data = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass 
    data["last_active_tracker"] = tracker_id
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def get_last_tracker_id() -> int:
    if not os.path.exists(CONFIG_FILE):
        return 0
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_active_tracker", 0)
    except (json.JSONDecodeError, FileNotFoundError):
        return 0