import os
from database import get_db, engine, Base
from services import TrackerService

# Remove o banco de dados existente
db_url = engine.url
if db_url.drivername == "sqlite":
    db_path = db_url.database
    if db_path and os.path.exists(db_path):
        os.remove(db_path)
        print(f"Banco de dados removido: {db_path}")

# Recria todas as tabelas
Base.metadata.create_all(bind=engine)
print("Banco de dados recriado com sucesso!")

try:
    with get_db() as db:
        tracker_service = TrackerService(db)
        tracker_service.create_tracker(name="Marcador padrão")

except Exception as e:
    print(f"Erro ao popular banco: {e}")