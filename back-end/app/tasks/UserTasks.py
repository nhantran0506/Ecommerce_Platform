from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.Users import User
from models.Authentication import Authentication
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db_connector import SessionLocal

class UserTasks:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.delete_inactive_users, 'interval', hours=24)
        self.scheduler.start()

    async def delete_inactive_users(self):
        db = SessionLocal()
        try:
            fourteen_days_ago = datetime.now() - timedelta(days=14)
            inactive_users = db.query(User).filter(
                User.is_deleted == True,
                User.deleted_date <= fourteen_days_ago
            ).all()

            for user in inactive_users:
                db.query(Authentication).filter(Authentication.user_id == user.id).delete()
                db.delete(user)

            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()
