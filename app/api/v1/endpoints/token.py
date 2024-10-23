from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.v1.dependencies.db_dependencies import DatabaseDep
from app.models.users import UserModel
from app.core.security import create_access_token, verify_password

router = APIRouter(tags=['Authentication'], prefix="/api")

@router.post("/token")
async def login_for_access_token(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    db : DatabaseDep
):
    user: UserModel = db.query(UserModel).filter(UserModel.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    token = create_access_token({"user_id" : user.id, "role" : user.role})

    return {"access_token" : token, "token_type" : "bearer"}
