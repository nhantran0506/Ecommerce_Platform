from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.Users import User
from models.Authentication import Authentication
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, delete
import logging

logger = logging.getLogger(__name__)

class UserTasks:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.delete_inactive_users, 'interval', hours=24)
        self.scheduler.start()

    async def delete_inactive_users(self):
        async with SessionLocal() as db:
            try:
                fourteen_days_ago = datetime.now() - timedelta(days=14)
                
                query = select(User).where(
                    User.deleted_date <= fourteen_days_ago
                )
                result = await db.execute(query)
                inactive_users = result.scalars().all()

                for user in inactive_users:
                    auth_delete_query = delete(Authentication).where(Authentication.user_id == user.user_id)
                    await db.execute(auth_delete_query)
                    user_delete_query = delete(User).where(User.user_id == user.user_id)
                    await db.execute(user_delete_query)

                await db.commit()
            except Exception as e:
                await db.rollback()
                logger.error(str(e))