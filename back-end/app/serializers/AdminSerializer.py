from pydantic import BaseModel
from datetime import datetime as Datetime

class AdminGetData(BaseModel):
    timestamp : str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True