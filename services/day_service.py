from database import get_db
from repositories import DayRepository
from dtos import DayDTO

class DayService:
    def get_day_by_id(self, day_id: int) -> DayDTO | None:
        with get_db() as db:
            day_repository = DayRepository(db)
            day = day_repository.get_day_by_id(day_id)
            if not day:
                return None
            return DayDTO.from_entity(day)
    
    def get_day_number(self, day_id: int) -> DayDTO | None:
        with get_db() as db:
            day_repository = DayRepository(db)
            day = day_repository.get_day_number(day_id)
            if not day:
                return None
            return DayDTO.from_entity(day)

    def check_day(self, day_id: int) -> DayDTO | None:
        with get_db() as db:
            day_repository = DayRepository(db)
            # Como a checagem e a ação ocorrem juntas na regra de negócio, 
            # fazemos isso dentro da mesma conexão do context manager.
            if not day_repository.get_day_by_id(day_id):
                return None
            day = day_repository.check_day(day_id)
            return DayDTO.from_entity(day)
    
    def get_specific_day(self, tracker_id: int, year: int, month: int, day: int) -> DayDTO | None:
        with get_db() as db:
            day_repository = DayRepository(db)
            day_entity = day_repository.get_specific_day(tracker_id, year, month, day)
            if not day_entity:
                return None
            return DayDTO.from_entity(day_entity)