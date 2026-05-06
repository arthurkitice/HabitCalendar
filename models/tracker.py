from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Tracker(Base):
    __tablename__ = "trackers"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    years = relationship(
        "Year", 
        backref="tracker", 
        order_by="Year.number.asc()", 
        cascade="all, delete-orphan", 
        passive_deletes=True
    )

    def __repr__(self):
        return f"Tracker(id={self.id}, name='{self.name}')"