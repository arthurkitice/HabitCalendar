from sqlalchemy.orm import Session
from models import Tracker, Month, Day
from dtos import TrackerDTO, TrackerWithMonthsDTO, MonthDTO
from constants import STARTING_YEAR, MONTHS
from helper import get_days

class TrackerRepository:
    def __init__(self, db: Session):
        self.db = db

    def _populate_tracker(self, tracker_id: int) -> None:
        for month_number in range(1, 13):
            month_name = MONTHS[month_number]
            month = Month(
                name=month_name,
                number=month_number,
                year=STARTING_YEAR,
                tracker_id=tracker_id
            )
            self.db.add(month)
            self.db.flush() 

            for day in get_days(STARTING_YEAR, month_number):
                day = Day(number=day, checked=False, month_id=month.id)
                self.db.add(day)

        self.db.commit()

    def get_tracker_by_id(self, tracker_id: int):
        return self.db.query(Tracker).filter(Tracker.id == tracker_id).first()

    def get_tracker_by_name(self, tracker_name: str):
        return self.db.query(Tracker).filter(Tracker.name == tracker_name).first()
    
    def get_all_trackers(self) -> list[Tracker]:
        return self.db.query(Tracker).all()

    def get_tracker_name(self, tracker_id: int):
        return self.db.query(Tracker).filter(Tracker.id == tracker_id).first().name

    def create_tracker(self, name: str):
        if self.get_tracker_by_name(name):
            return None

        tracker = Tracker(name=name)
        self.db.add(tracker)
        self.db.commit()
        self.db.refresh(tracker)

        self._populate_tracker(tracker_id=tracker.id)

        return tracker
    
    def update_tracker(self, tracker_id: int, name: str):
        tracker = self.get_tracker_by_id(tracker_id)
        tracker.name = name
        self.db.commit()
        self.db.refresh(tracker)

        return tracker

    def delete_tracker(self, tracker_id: int):
        tracker = self.get_tracker_by_id(tracker_id)
        self.db.delete(tracker)
        self.db.commit()
