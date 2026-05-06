from functools import wraps
from database import get_db
from services import MonthService, YearService

def handle_db(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            with get_db() as db:
                # Injeta a conexão 'db' pronta para a função original usar
                return method(self, db, *args, **kwargs)
        except Exception as e:
            # O tratamento de erro genérico fica em um ÚNICO lugar do projeto inteiro!
            print(f"Falha na operação '{method.__name__}': {e}")
            return None
    return wrapper

class YearController:
    @handle_db
    def get_years(self, db, tracker_id: int) -> list[int]:
        year_service = YearService(db)
        return year_service.get_years_from_tracker(tracker_id)

    @handle_db
    def add_year(self, db, tracker_id: int, year: int) -> bool | None:
        year_service = YearService(db)
        return year_service.add_tracker_year(tracker_id=tracker_id, year_number=year)

    @handle_db
    def get_month_id(self, db, tracker_id: int,  year: int, month_number: int) -> int| None:
        month_service = MonthService(db)
        return month_service.get_specific_month(tracker_id, year, month_number).id