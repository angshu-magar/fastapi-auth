from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.base import Base

class PermissionModel(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    permission = Column(ARRAY(Integer), nullable=False)

    resource_id = Column(Integer, ForeignKey('resources.id'))
    resource = relationship('ResourceModel', uselist=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship('RoleModel', back_populates='perms', uselist=False)
