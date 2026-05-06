from functools import wraps
from database import get_db
from services import TrackerService, MonthService, DayService, YearService
from dtos import DayDTO, MonthDTO, TrackerDTO

# 1. CRIAMOS O DECORADOR (A "fábrica" de conexões e tratamento de erro)
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

class CalendarController:
    @handle_db
    def get_trackers(self, db) -> list[TrackerDTO] | None:
        tracker_service = TrackerService(db)
        return tracker_service.get_all_trackers()

    @handle_db
    def create_tracker(self, db, name: str) -> TrackerDTO | None:
        tracker_service = TrackerService(db)
        return tracker_service.create_tracker(name=name)
    
    @handle_db
    def get_days(self, db, month_id: int) -> list[DayDTO] | None:
        month_service = MonthService(db)
        return month_service.get_month_with_days(month_id).days
    
    @handle_db
    def get_specific_days(self, db, tracker_id: int, year: int, month: int) -> list[DayDTO] | None:
        """Retorna os dias específicos de um mês, baseado no ano e id do tracker"""
        month_service = MonthService(db)
        return month_service.get_specific_month_with_days(tracker_id=tracker_id, year=year, month_number=month).days

    @handle_db
    def get_tracker_by_id(self, db, tracker_id: int) -> TrackerDTO | None:
        tracker_service = TrackerService(db)
        return tracker_service.get_tracker_by_id(tracker_id)

    @handle_db
    def check_day(self, db, tracker_id: int, year: int, month: int, day: int) -> DayDTO | None:
        day_service = DayService(db)
        day = day_service.get_specific_day(tracker_id, year, month, day)
        return day_service.check_day(day.id)

    @handle_db
    def get_years(self, db, tracker_id: int) -> list[int]:
        year_service = YearService(db)
        return year_service.get_years_from_tracker(tracker_id)

    @handle_db
    def add_year(self, db, tracker_id: int, year: int) -> bool | None:
        year_service = YearService(db)
        return year_service.add_tracker_year(tracker_id=tracker_id, year_number=year)
    
    @handle_db
    def edit_tracker(self, db, tracker_id: int, name: str) -> TrackerDTO | None:
        tracker_service = TrackerService(db)
        return tracker_service.update_tracker(tracker_id=tracker_id, name=name)

    @handle_db
    def remove_tracker(self, db, tracker_id: int) -> bool:
        tracker_service = TrackerService(db)
        return tracker_service.delete_tracker(tracker_id)
    
    @handle_db
    def get_specific_month(self, db, tracker_id: int, year: int, month_number: int) -> MonthDTO | None:
        month_service = MonthService(db)
        return month_service.get_specific_month(tracker_id, year, month_number)