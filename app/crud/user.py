from bson import ObjectId
from typing import Optional


async def get_user_by_email(db, email: str) -> Optional[dict]:
    user = await db["users"].find_one({"email": email})

    if user:
        user["id"] = str(user["_id"])
        user.pop("_id", None)

    return user


async def create_user_by_email(db, user_data: dict) -> dict:
    result = await db["users"].insert_one(user_data)
    new_user = await db["users"].find_one({"_id": result.inserted_id})
    if new_user:
        new_user["id"] = str(new_user["_id"])
        new_user.pop("_id", None)
    return new_user
