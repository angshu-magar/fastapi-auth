from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)

    perms = relationship('PermissionModel', back_populates='role')
    users = relationship('UserModel', back_populates='role')
