from fastapi import APIRouter, status, Depends
from app.models.userModel import PersonModel, UserModel
from app.api.v1.dependencies.db_dependencies import DatabaseDep
from app.schemas.userSchema import UserCreate
from app.core.security import hash_password, decode_token
from typing import Annotated

router = APIRouter(tags=['Nothing'])

# @router.post("/create-user", status_code=status.HTTP_201_CREATED)
# async def create_user(db: DatabaseDep, user: UserCreate):
    # user.password = hash_password(user.password)
    # u : UserModel = UserModel(
        # username = user.username,
        # password = user.password,
    # )
    # p : PersonModel = PersonModel(
        # name = user.name,
        # user = u
    # )
    # db.add(u)
    # db.add(p)
    # db.commit()
    # return {'message': 'created'}

@router.get("/me")
async def test1():
    return {"message" : "You have view permission"}

@router.post("/me")
async def test2():
    return {"message" : "You have create permission"}

@router.put("/me")
async def test3():
    return {"message" : "You have update permission"}

@router.delete("/me")
async def test4():
    return {"message" : "You have delete permission"}
