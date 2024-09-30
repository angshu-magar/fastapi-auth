from datetime import datetime
from pydantic import BaseModel

# TODO
# Check if datetime maps to sqlalchemy's DateTime
class Attendance(BaseModel):
    start : datetime
    end : datetime
    time_delta : float
    user_id : int
    food : str
    food_price : float
