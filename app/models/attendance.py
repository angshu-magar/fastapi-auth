from ..db.base import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

class AttendanceModel(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, nullable=False)
    start = Column(DateTime)
    end = Column(DateTime)
    time_delta = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food = Column(String(100))
    food_price = Column(Float)
