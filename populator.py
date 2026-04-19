from database import get_db
from repositories import DayRepository, MonthRepository
from helper import get_days, get_month_name

YEAR = 2026
MONTHS = 12
STARTING_MONTH = 1

def populate_tracker(db, tracker):
    try:
        day_repository = DayRepository(db)
        month_repository = MonthRepository(db)

        # Criação dos meses
        for month_number in range(STARTING_MONTH, MONTHS + 1):
            month_name = get_month_name(month_number)
            month = month_repository.create_month(name=month_name, number=month_number, year=YEAR, tracker_id=tracker.id)

            for day in get_days(YEAR, month_number):
                day_repository.create_day(number=day, checked=False, month_id=month.id)
    

    except Exception as e:
        print(f"Erro ao popular banco: {e}")