from app.db.base import Base
from sqlalchemy import Column, Integer, String

class BasicUserModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)

class UserModel(BasicUserModel):
    __tablename__ = 'users'
