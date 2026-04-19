from sqlalchemy.orm import Session
from models import Tracker, Month
from dtos import TrackerDTO, TrackerWithMonthsDTO, MonthDTO
from populator import populate_tracker

class TrackerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tracker_by_id(self, tracker_id: int):
        return self.db.query(Tracker).filter(Tracker.id == tracker_id).first()
    
    def get_dto_tracker_by_id(self, tracker_id: int):
        tracker = self.db.query(Tracker).filter(Tracker.id == tracker_id).first()
        return TrackerDTO(
            id=tracker.id,
            name=tracker.name
        )

    def get_tracker_by_name(self, tracker_name: str):
        tracker = self.db.query(Tracker).filter(Tracker.name == tracker_name).first()
        if tracker:
            return TrackerDTO(
                id=tracker.id,
                name=tracker.name
            )
        return None
    
    def get_all_trackers(self):
        trackers = self.db.query(Tracker).all()
        return [
            TrackerDTO(
                id=tracker.id,
                name=tracker.name
            ) for tracker in trackers
        ]

    def get_tracker_name(self, tracker_id: int):
        return self.db.query(Tracker).filter(Tracker.id == tracker_id).first().name

    def create_tracker(self, name: str):
        if self.get_tracker_by_name(name):
            return None

        new_tracker = Tracker(name=name)
        self.db.add(new_tracker)
        self.db.commit()
        self.db.refresh(new_tracker)
        
        tracker = TrackerDTO(
            id=new_tracker.id, 
            name=new_tracker.name
        )

        populate_tracker(db=self.db, tracker=tracker)

        return tracker
    
    def update_tracker(self, tracker_id: int, name: str):
        tracker = self.get_tracker_by_id(tracker_id)
        if tracker:
            tracker.name = name
            self.db.commit()
            self.db.refresh(tracker)
            return TrackerDTO(
                id=tracker.id, 
                name=tracker.name
            )
        return None
    
    def delete_tracker(self, tracker_id: int):
        tracker = self.get_tracker_by_id(tracker_id)
        if tracker:
            self.db.delete(tracker)
            self.db.commit()
            return True
        return False

    def get_tracker_with_months_by_id(self, tracker_id: int):
        tracker = self.get_tracker_by_id(tracker_id)
        if tracker:
            months = [
                MonthDTO(
                    id=m.id, 
                    name=m.name,
                    number=m.number,
                    year=m.year,
                    tracker_id=m.tracker_id
                ) 
                for m in tracker.month
            ]
            return TrackerWithMonthsDTO(
                id=tracker.id,
                name=tracker.name,
                months=months
            )
        return None