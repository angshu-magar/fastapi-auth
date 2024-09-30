from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.v1.dependencies.db_dependencies import DatabaseDep
from app.models.user import UserModel
from app.core.security import hash_password, create_access_token, oauth2_scheme

router = APIRouter(tags=['Authentication'])

@router.post("/token")
async def login_for_access_token(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    db : DatabaseDep
):
    input_hashed_password = hash_password(form_data.password)
    user: UserModel = db.query(UserModel).filter(
        UserModel.email == form_data.username,
        UserModel.password == input_hashed_password
    ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    token = create_access_token({"user_id" : user.id})

    return {"access_token" : token, "token_type" : "bearer"}
