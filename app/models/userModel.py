from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_login = Column(Boolean, default=True)
    person = relationship('PersonModel', back_populates='user', uselist=False)

    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('RoleModel', back_populates='users', uselist=False)

class PersonModel(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserModel', back_populates='person', uselist=False)
