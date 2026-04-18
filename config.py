import json
import os

CONFIG_FILE = "app_settings.json"

def get_last_month_index():
    """Lê o índice do último mês visualizado."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("current_month_index", 0)
        except (json.JSONDecodeError, IOError):
            return 0
    return 0

def save_current_month_index(index):
    """Salva o índice atual no arquivo JSON."""
    data = {"current_month_index": index}
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Erro ao salvar configurações: {e}")