from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from datetime import datetime
import logging
import shutil
import os

def get_app_dir() -> str:
    app_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "HabitCalendar")
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

APP_DIR = get_app_dir()
DATABASE_URL = f"sqlite:///{os.path.join(APP_DIR, 'database.db')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

logger = logging.getLogger(__name__)
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Falha na operação de banco: {e}", exc_info=True)
        raise
    finally:
        db.close()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

BACKUP_PATH = os.path.join(APP_DIR, 'database.habitbackup')
DB_PATH = os.path.join(APP_DIR, 'database.db')
REQUIRED_TABLES = {'trackers', 'years', 'months', 'days'}

def create_backup() -> bool:
    try:
        shutil.copy2(DB_PATH, BACKUP_PATH)
        logging.getLogger(__name__).info(f"Backup criado em {BACKUP_PATH}")
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao criar backup: {e}", exc_info=True)
        return False

def validate_backup(path: str) -> bool:
    try:
        from sqlalchemy import create_engine, inspect
        engine = create_engine(f"sqlite:///{path}")
        tables = set(inspect(engine).get_table_names())
        return REQUIRED_TABLES.issubset(tables)
    except:
        return False

def restore_backup() -> bool:
    try:
        if not os.path.exists(BACKUP_PATH):
            return False
        if not validate_backup(BACKUP_PATH):
            return False
        shutil.copy2(DB_PATH, DB_PATH + '.pre_restore')  # segurança extra
        shutil.copy2(BACKUP_PATH, DB_PATH)
        logging.getLogger(__name__).info("Backup restaurado com sucesso")
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Erro ao restaurar backup: {e}", exc_info=True)
        return False

def get_backup_info() -> dict | None:
    if not os.path.exists(BACKUP_PATH):
        return None
    modified = os.path.getmtime(BACKUP_PATH)
    return {
        "date": datetime.fromtimestamp(modified).strftime("%d/%m/%Y %H:%M")
    }