from jose import jwt,JWTError
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from . import db, schemas, models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "hello"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    return id

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(db.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User credentials not valid",headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token).first()
    return user