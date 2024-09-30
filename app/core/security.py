from typing import Annotated
from fastapi import HTTPException, status, Depends
import hashlib, jwt
from jwt.exceptions import InvalidTokenError

from app.api.v1.dependencies.db_dependencies import DatabaseDep
from app.models.user import UserModel
from .config import settings
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password : str) -> str:
    salt = settings.salt
    password_encoded = password.encode()
    if salt:
        password_encoded +=  salt.encode()
    hash_object = hashlib.sha256(password_encoded)
    return hash_object.hexdigest()

def verify_password(input_raw_password : str, hashed_password : str) -> bool:
    input_hashed = hash_password(input_raw_password)
    return input_hashed == hashed_password

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def get_current_user(
    token : Annotated[str, Depends(oauth2_scheme)],
    db : DatabaseDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithm=settings.algorithm)
        print(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        print("Hello")
        raise credentials_exception

    user : UserModel = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user
