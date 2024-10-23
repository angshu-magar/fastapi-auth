from typing import Annotated
from fastapi import HTTPException, status, Depends
import jwt
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from app.models.users import UserModel
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from app.api.v1.dependencies.db_dependencies import DatabaseDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)

def hash_password(password : str) -> str:
    return pwd_context.hash(password)

def verify_password(input_raw_password : str, hashed_password : str) -> bool:
    return pwd_context.verify(input_raw_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_token(_kmstoken : Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(_kmstoken, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("user_id")
        role = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="decode token")
    return {"user_id" : user_id, "role" : role}


async def get_current_user(
    tokenInfo : Annotated[dict, Depends(decode_token)],
    db : DatabaseDep
):
    user : UserModel = db.query(UserModel).filter(UserModel.id == tokenInfo.get("user_id")).first()
    if user is None:
        raise credentials_exception

    return user

# class RoleChecker:
    # def __init__(self, *roles : str):
        # self.allowed_roles = []
        # self.allowed_roles.extend(roles)

    # def __call__(self,tokenInfo : Annotated[dict, Depends(decode_token)]):
        # if tokenInfo.get("role") in self.allowed_roles:
            # return tokenInfo

        # raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT, detail="Redirecting to login", headers={"Location": "/login"})
