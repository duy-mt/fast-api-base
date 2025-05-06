from motor.motor_asyncio import AsyncIOMotorClient
from ..config.index import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

db = client[settings.DATABASE]


async def get_db():
    return db
