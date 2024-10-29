from app.db.session import get_db, engine
from app.db.base import Base
from app.models.userModel import PersonModel, UserModel
from app.core.security import hash_password
from app.models.permissionModel import PermissionModel
from app.models.resourceModel import ResourceModel
from app.models.roleModel import RoleModel

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
db = next(get_db())

role = RoleModel(
    label = "level1"
)
db.add(role)
db.commit()
db.refresh(role)

u = UserModel(
    username = "user1",
    password = hash_password("password"),
    role_id = role.id
)

db.add(u)
db.commit()
db.refresh(u)

p = PersonModel(
    name = "Angshu",
    user_id = u.id
)
db.add(p)


res = ResourceModel(
    resourceName = "me"
)
db.add(res)

db.commit()
db.refresh(role)
db.refresh(res)

perm = PermissionModel(
    permission = [0, 0, 1, 1],
    resource_id = res.id,
    role_id = role.id

)
db.add(perm)
db.commit()
