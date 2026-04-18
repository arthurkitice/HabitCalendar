from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import relationship
from database import Base

class Month(Base):
    __tablename__ = "months"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(Integer)

    day = relationship("Day", back_populates="month")

    def __repr__(self):
        return f"Month(id={self.id}, name='{self.name}', number={self.number})"