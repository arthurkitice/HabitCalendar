from sqlalchemy.orm import Session
from repositories import TrackerRepository
from dtos import TrackerDTO, TrackerWithYearsDTO

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
    
    def get_tracker_with_years_by_id(self, tracker_id: int) -> TrackerWithYearsDTO | None:
        tracker = self.tracker_repository.get_tracker_by_id(tracker_id)

        if not tracker:
            return None
        
        return TrackerWithYearsDTO.from_entity(tracker)
    
    def get_tracker_with_years_by_name(self, tracker_name: str) -> TrackerWithYearsDTO | None:
        tracker = self.tracker_repository.get_tracker_by_name(tracker_name)
        
        if not tracker:
            return None
        
        return TrackerWithYearsDTO.from_entity(tracker)
    
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
