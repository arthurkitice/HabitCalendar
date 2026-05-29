from contextlib import contextmanager
import os, logging, sys
import sqlite3

def get_save_directory():
    """Retorna o caminho correto para salvar os dados conforme o SO atual."""
    app_name = "HabitCalendar"
    
    if sys.platform == "win32":
        # Windows: Usa AppData\Local (ideal para dados locais/banco de dados)
        # Tenta pegar a variável de ambiente LOCALAPPDATA, se não achar, usa o fallback manual
        base_dir = os.environ.get("LOCALAPPDATA") or os.path.expanduser(r"~\AppData\Local")
        return os.path.join(base_dir, app_name)
        
    elif sys.platform == "darwin":
        # macOS: O padrão correto para dados de suporte do app
        return os.path.expanduser(f"~/Library/Application Support/{app_name}")
        
    else:
        # Linux e outros sistemas Unix-like
        # Tenta seguir a especificação XDG, senão usa o fallback tradicional
        base_dir = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
        return os.path.join(base_dir, app_name)

APP_DIR = get_save_directory()

os.makedirs(APP_DIR, exist_ok=True)

DB_PATH = os.path.join(APP_DIR, 'database.db')

logger = logging.getLogger(__name__)
@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Falha na operação de banco: {e}", exc_info=True)
        raise
    finally:
        conn.close()
