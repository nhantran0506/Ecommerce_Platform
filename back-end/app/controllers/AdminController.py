
from sqlalchemy.orm import Session
from models.Users import User, UserRoles
from models.Authentication import Authentication
from serializers.UserSearializers import *
from middlewares.token_config import *
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import UUID
from fastapi import status, Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from models.Shop import Shop
from sqlalchemy.ext.asyncio import AsyncSession

class AdminController:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def get_revenue(self, timestamp):
        pass

    async def statistics_product_category(self, category_name: str, timestamp: datetime):
        pass # -> quantity, total

    async def get_shop_number(self):
        query = select(func.count()).select_from(Shop)  
        result = await self.db.execute(query)
        shop_count = result.scalar()
        return shop_count


