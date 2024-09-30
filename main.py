from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.v1.endpoints import user, token

app = FastAPI()
app.include_router(user.router)
app.include_router(token.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message":"Hello World"}
