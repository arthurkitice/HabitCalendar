import os
from database import get_db, engine, Base
from repositories import DayRepository, MonthRepository, TrackerRepository
from dtos import DayDTO, MonthDTO
from helper import get_days, get_month_name

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

YEAR = 2026
MONTHS = 12
STARTING_MONTH = 1

try:
    with get_db() as db:
        day_repository = DayRepository(db)
        month_repository = MonthRepository(db)
        tracker_repository = TrackerRepository(db)

        tracker_repository.create_tracker(name="Marcador padrão")

        # Criação dos meses
        for month_number in range(STARTING_MONTH, MONTHS + 1):
            month_name = get_month_name(month_number)
            month = month_repository.create_month(name=month_name, number=month_number, year=YEAR, tracker_id=1)
            print(f"Mês {month_name} criado com sucesso!")

            for day in get_days(YEAR, month_number):
                day_repository.create_day(number=day, checked=False, month_id=month.id)
            print(f"Dias do mês {month_name} criados com sucesso!")

        print(f"Dias de dezembro: {month_repository.get_days_by_month_number(12)}")

except Exception as e:
    print(f"Erro ao popular banco: {e}")