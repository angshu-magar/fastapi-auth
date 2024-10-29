from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.dialects.postgresql import ARRAY

class ResourceModel(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    resourceName = Column(String, nullable=False)
