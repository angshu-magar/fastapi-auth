from typing import Annotated

from fastapi import Depends
from app.db.session import get_db, SessionLocal


DatabaseDep = Annotated[SessionLocal, Depends(get_db)]
