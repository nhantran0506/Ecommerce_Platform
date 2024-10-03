from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class CartModify(BaseModel):
    product_id : UUID
    quantity : int



