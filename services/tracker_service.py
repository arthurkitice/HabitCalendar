from database import get_connection
from repositories import TrackerRepository, YearRepository
from models import Tracker
from datetime import datetime

class TrackerService:
    def get_tracker_by_id(self, tracker_id: int) -> Tracker | None:
        with get_connection() as conn:
            return TrackerRepository(conn).get_tracker_by_id(tracker_id)

    def get_tracker_by_name(self, tracker_name: str) -> Tracker | None:
        with get_connection() as conn:
            return TrackerRepository(conn).get_tracker_by_name(tracker_name)
    
    def get_all_trackers(self) -> list[Tracker] | None:
        with get_connection() as conn:
            return TrackerRepository(conn).get_all_trackers()

    def get_tracker_name(self, tracker_id: int) -> str | None:
        with get_connection() as conn:
            tracker = TrackerRepository(conn).get_tracker_by_id(tracker_id)

            if tracker is None:
                return None
            
            return tracker.name

    def create_tracker(self, name: str) -> Tracker | None:
        if not name:
            return None
        with get_connection() as conn:
            new_tracker = TrackerRepository(conn).create_tracker(name)

            if new_tracker is not None:
                YearRepository(conn).create_year_with_cascade(tracker_id=new_tracker.id, year_number=datetime.now().year)

            return new_tracker
        
    def update_tracker(self, tracker_id: int, name: str) -> Tracker | None:
        with get_connection() as conn:
            return TrackerRepository(conn).update_tracker(tracker_id, name)

    def delete_tracker(self, tracker_id: int) -> bool:
        with get_connection() as conn:
            return TrackerRepository(conn).delete_tracker(tracker_id)
    
    def get_checked_days_count(self, tracker_id: int) -> int | None:
        with get_connection() as conn:
            return TrackerRepository(conn).get_all_checked_days(tracker_id)