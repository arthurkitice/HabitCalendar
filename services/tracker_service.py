from sqlalchemy.orm import Session
from repositories import TrackerRepository
from dtos import TrackerDTO, TrackerWithMonthsDTO

MIN_YEAR = 2000
MAX_YEAR = 2100

class TrackerService:
    def __init__(self, db: Session):
        self.db = db
        self.tracker_repository = TrackerRepository(self.db)

    def get_tracker_by_id(self, tracker_id: int) -> TrackerDTO | None:
        tracker = self.tracker_repository.get_tracker_by_id(tracker_id)

        if not tracker:
            return None
        
        return TrackerDTO.from_entity(tracker)

    def get_tracker_by_name(self, tracker_name: str) -> TrackerDTO | None:
        tracker = self.tracker_repository.get_tracker_by_name(tracker_name)
        
        if not tracker:
            return None
        
        return TrackerDTO.from_entity(tracker)
    
    def get_tracker_with_months_by_id(self, tracker_id: int) -> TrackerWithMonthsDTO | None:
        tracker = self.tracker_repository.get_tracker_by_id(tracker_id)

        if not tracker:
            return None
        
        return TrackerWithMonthsDTO.from_entity(tracker)
    
    def get_tracker_with_months_by_name(self, tracker_name: str) -> TrackerWithMonthsDTO | None:
        tracker = self.tracker_repository.get_tracker_by_name(tracker_name)
        
        if not tracker:
            return None
        
        return TrackerWithMonthsDTO.from_entity(tracker)
    
    def get_all_trackers(self) -> list[TrackerDTO] | None:
        trackers = self.tracker_repository.get_all_trackers()
        
        if not trackers:
            return None
        
        return [TrackerDTO.from_entity(t) for t in trackers]

    def get_tracker_name(self, tracker_id: int) -> str | None:
        if self.get_tracker_by_id(tracker_id):
            return self.tracker_repository.get_tracker_name(tracker_id)
        return None

    def create_tracker(self, name: str) -> TrackerDTO | None:
        if name:
            tracker = self.tracker_repository.create_tracker(name)
            return TrackerDTO.from_entity(tracker)
        return None
    
    def add_tracker_year(self, tracker_id: int, year: int) -> bool | None:
        if not self.get_tracker_by_id(tracker_id):
            return None

        if not (MIN_YEAR <= year <= MAX_YEAR):
            return False #Ano fora do intervalo válido
        
        return self.tracker_repository.add_tracker_year(tracker_id=tracker_id, year=year)

    def update_tracker(self, tracker_id: int, name: str) -> TrackerDTO | None:
        if self.get_tracker_by_id(tracker_id):
            tracker = self.tracker_repository.update_tracker(tracker_id, name)
            return TrackerDTO.from_entity(tracker)
        return None

    def delete_tracker(self, tracker_id: int) -> bool:
        if self.get_tracker_by_id(tracker_id):
            self.tracker_repository.delete_tracker(tracker_id)
            return True
        return False
