from contextlib import contextmanager
import os, logging
import sqlite3

def get_app_dir() -> str:
    app_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "HabitCalendar")
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

APP_DIR = get_app_dir()
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
