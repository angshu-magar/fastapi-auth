from fastapi import APIRouter, status, Depends
from app.models.user import UserModel
from app.api.v1.dependencies.db_dependencies import DatabaseDep
from app.schemas import user
from app.core.security import hash_password, get_current_user
from typing import Annotated

router = APIRouter(tags=['Authentication'])
@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(db: DatabaseDep, user: user.BasicUser):
    user.password = hash_password(user.password)
    # print(**user.model_dump())
    u : UserModel = UserModel(**user.model_dump())
    db.add(u)
    db.commit()
    return {'message': 'created'}

@router.get("/me")
async def my_data(me : Annotated[UserModel, Depends(get_current_user)]):
    return me
