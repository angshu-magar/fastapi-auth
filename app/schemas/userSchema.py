from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username : str
    password : str = Field(min_length=8, max_length=150)

    name : str
