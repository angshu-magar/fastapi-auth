from ..db.base import Base
from sqlalchemy import Column, Integer, String

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    name = Column(String(150), nullable=False)
    role = Column(String(150), nullable=False)
    contact = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    email2 = Column(String(150))
    photo = Column(String(150), nullable=False)
    emergency_contact = Column(String(150), nullable=False)
    emergency_phone = Column(String(150), nullable=False)
    status = Column(Integer, nullable=False)

