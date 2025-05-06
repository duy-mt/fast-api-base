from ..core.database import get_db


async def delete_sessions_without_chats():
    db = await get_db()

    result = await db["chatsessions"].delete_many(
        {"$or": [{"chats": {"exists": False}}, {"chats": {"$size": 0}}]}
    )

    print(f"[CRON] Deleted {result.deleted_count} sessions without chats.")
