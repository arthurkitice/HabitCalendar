from contextlib import contextmanager
import os, logging, sys
import sqlite3

def get_save_directory():
    """Retorna o caminho correto para salvar os dados conforme o SO atual."""
    app_name = "HabitCalendar"
    
    if sys.platform == "win32":
        base_dir = os.environ.get("LOCALAPPDATA") or os.path.expanduser(r"~\AppData\Local")
        return os.path.join(base_dir, app_name)
        
    elif sys.platform == "darwin":
        return os.path.expanduser(f"~/Library/Application Support/{app_name}")
        
    else:
        base_dir = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
        return os.path.join(base_dir, app_name)

APP_DIR = get_save_directory()
os.makedirs(APP_DIR, exist_ok=True)
DB_PATH = os.path.join(APP_DIR, 'database.db')

logger = logging.getLogger(__name__)

# --- INÍCIO DA OTIMIZAÇÃO ---
# Variável global para manter a conexão viva durante toda a vida do app
_global_conn = None

def _get_persistent_connection():
    global _global_conn
    if _global_conn is None:
        _global_conn = sqlite3.connect(DB_PATH)
        _global_conn.row_factory = sqlite3.Row
        
        # Otimizações vitais para HDDs mecânicos
        _global_conn.execute("PRAGMA journal_mode = WAL")      # Escrita sequencial super rápida
        _global_conn.execute("PRAGMA synchronous = NORMAL")    # Segurança contra crashes sem travar o HD
        _global_conn.execute("PRAGMA foreign_keys = ON")
    
    return _global_conn

def close_global_connection():
    """Fecha explicitamente a conexão persistente para permitir operações de arquivo (como restauração de backup)."""
    global _global_conn
    if _global_conn is not None:
        try:
            _global_conn.close()
        except Exception:
            pass
        _global_conn = None

@contextmanager
def get_connection():
    """Fornece a conexão persistente e gerencia apenas a transação (commit/rollback)"""
    conn = _get_persistent_connection()
    try:
        yield conn
        conn.commit()  # Salva a alteração imediatamente (Seguro contra queda de energia)
    except Exception as e:
        conn.rollback()
        logger.error(f"Falha na operação de banco: {e}", exc_info=True)
        raise
    # REMOVIDO: conn.close() -> O arquivo agora fica aberto na memória RAM!