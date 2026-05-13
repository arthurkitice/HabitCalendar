from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from contextlib import contextmanager  # ← ADICIONE ESTA LINHA

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        # Tratamento centralizado! Você pode usar um logger real aqui no futuro
        print(f"[Database Error]: Falha na operação. Detalhes: {e}")
        # traceback.print_exc() # Útil para debug no terminal
        raise # Opcional: propaga o erro se você quiser que o Service saiba que falhou, ou remova o 'raise' para engolir o erro silenciosamente.
    finally:
        db.close()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()