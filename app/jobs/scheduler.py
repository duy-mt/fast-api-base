from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..jobs.cleanup import delete_sessions_without_chats

scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.add_job(delete_sessions_without_chats, "interval", minutes=30)
    scheduler.start()
