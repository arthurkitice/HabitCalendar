from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Month(Base):
    __tablename__ = "months"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(Integer)
    year_id = Column(Integer, ForeignKey("years.id", ondelete='CASCADE')) 

    days = relationship("Day", backref="month", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"Month(id={self.id}, name='{self.name}', number={self.number}, year_id={self.year_id})"