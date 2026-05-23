from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from contextlib import contextmanager
import os, logging

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

