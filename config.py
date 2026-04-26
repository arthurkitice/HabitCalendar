import json
import os

CONFIG_FILE = "app_settings.json"

def get_last_month_index(tracker_id: int) -> int:
    if not os.path.exists(CONFIG_FILE):
        return 0
    
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            # Tenta pegar o índice usando o ID do tracker como string. Se não achar, retorna 0.
            return data.get(str(tracker_id), 0)
    except (json.JSONDecodeError, FileNotFoundError):
        return 0

def save_current_month_index(tracker_id: int, index: int) -> None:
    data = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass # Se o arquivo estiver corrompido, cria um novo dicionário
    
    # Atualiza ou cria a chave com o ID do tracker
    data[str(tracker_id)] = index
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def save_current_tracker_id(tracker_id: int) -> None:
    data = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass # Se o arquivo estiver corrompido, cria um novo dicionário
    
    # Cria uma chave específica de configuração chamada "last_active_tracker"
    data["last_active_tracker"] = tracker_id
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def get_last_tracker_id() -> int:
    if not os.path.exists(CONFIG_FILE):
        return 0
    
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            # Tenta pegar a chave que criamos. Se não existir, retorna 0 (Nenhum)
            return data.get("last_active_tracker", 0)
    except (json.JSONDecodeError, FileNotFoundError):
        return 0