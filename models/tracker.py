from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Tracker(Base):
    __tablename__ = "trackers"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    month = relationship("Month", back_populates="tracker")

    def __repr__(self):
        return f"Month(id={self.id}, name='{self.name}'"