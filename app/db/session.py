from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, engine
from .base import Base
from app.core.config import settings

engine = create_engine(settings.sqlalchemy_database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    Base.metadata.create_all(engine)
    try:
        yield db
    finally:
        db.close()

