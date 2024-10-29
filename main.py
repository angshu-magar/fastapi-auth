from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.v1.endpoints import user, token
from app.services.rbac import RBACMiddleware

app = FastAPI()
app.include_router(user.router)
app.include_router(token.router)

app.add_middleware(RBACMiddleware)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message":"Hello World"}


