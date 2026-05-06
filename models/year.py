from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Year(Base):
    __tablename__ = "years"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    tracker_id = Column(Integer, ForeignKey("trackers.id", ondelete='CASCADE')) 

    months = relationship(
        "Month",
        backref="year_ref", 
        order_by="Month.number.asc()",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f"Year(id={self.id}, number={self.number}, tracker_id={self.tracker_id})"