from fastapi import APIRouter, status, Depends
from app.models.users import PersonModel, UserModel
from app.api.v1.dependencies.db_dependencies import DatabaseDep
from app.schemas.user import UserCreate
from app.core.security import hash_password, get_current_user
from typing import Annotated

router = APIRouter(tags=['Authentication'])

@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(db: DatabaseDep, user: UserCreate):
    user.password = hash_password(user.password)
    u : UserModel = UserModel(
        username = user.username,
        password = user.password,
        role = user.role
    )
    p : PersonModel = PersonModel(
        name = user.name,
        age = user.age,
        user = u
    )
    db.add(u)
    db.add(p)
    db.commit()
    return {'message': 'created'}

@router.get("/me")
async def my_data(me : Annotated[UserModel, Depends(get_current_user)]):
    me.person
    return me
