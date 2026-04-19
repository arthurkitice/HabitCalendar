from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True)
    month_id = Column(Integer, ForeignKey("months.id", ondelete='CASCADE'))
    number = Column(Integer)
    checked = Column(Boolean, default=False)

    def __repr__(self):
        return f"Day(id={self.id}, number='{self.number}', checked='{self.checked}')"