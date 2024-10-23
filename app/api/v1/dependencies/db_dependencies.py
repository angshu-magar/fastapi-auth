from typing import Annotated

from fastapi import Depends
from app.db.session import get_db
from sqlalchemy.orm import Session


DatabaseDep = Annotated[Session, Depends(get_db)]
