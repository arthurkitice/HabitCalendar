from sqlalchemy.orm import Session
from models import Tracker
from .year_repository import YearRepository  # Importamos o repositório irmão
from datetime import datetime

class TrackerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tracker_by_id(self, tracker_id: int) -> Tracker | None:
        return self.db.query(Tracker).filter(Tracker.id == tracker_id).first()

    def get_tracker_by_name(self, tracker_name: str) -> Tracker | None:
        return self.db.query(Tracker).filter(Tracker.name == tracker_name).first()
    
    def get_all_trackers(self) -> list[Tracker]:
        return self.db.query(Tracker).all()

    def get_tracker_name(self, tracker_id: int) -> str | None:
        tracker = self.get_tracker_by_id(tracker_id)
        return tracker.name if tracker else None

    def create_tracker(self, name: str) -> Tracker | None:
        if self.get_tracker_by_name(name):
            return None

        tracker = Tracker(name=name)
        self.db.add(tracker)
        self.db.flush()

        # Por padrão, cada marcador criado inicia com o ano atual
        year_repo = YearRepository(self.db)
        current_year = datetime.now().year
        year_repo.create_year_with_cascade(tracker_id=tracker.id, year_number=current_year)

        return tracker

    def update_tracker(self, tracker_id: int, name: str) -> Tracker | None:
        tracker = self.get_tracker_by_id(tracker_id)
        if not tracker:
            return None
            
        tracker.name = name
        self.db.commit()
        self.db.refresh(tracker)
        return tracker

    def delete_tracker(self, tracker_id: int) -> bool:
        tracker = self.get_tracker_by_id(tracker_id)
        if not tracker:
            return False
            
        self.db.delete(tracker)
        self.db.commit()
        return True