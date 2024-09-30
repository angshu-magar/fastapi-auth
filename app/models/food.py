from ..db.base import Base
from sqlalchemy import Column, Integer, String, Float

class FoodModel(Base):
    __tablename__ = 'food'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
