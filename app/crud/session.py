from bson import ObjectId
from typing import Optional, List, Dict
from datetime import datetime, timezone


async def list_sessions_by_user(db, userId: str) -> List[Dict]:

    userId_obj = ObjectId(userId)

    cursor = db["chatsessions"].find({"userId": userId_obj}).sort("createdAt", -1)

    sessions = await cursor.to_list(length=None)

    if sessions:
        for session in sessions:
            session["id"] = str(session["_id"])
            session.pop("_id", None)

    return sessions


async def create_session_by_user(db, userId: str) -> Dict:

    userId_obj = ObjectId(userId)

    session_data = {
        "userId": userId_obj,
        "title": "New chat",
        "chats": [],
        "createdAt": datetime.now(timezone.utc),
    }

    result = await db["chatsessions"].insert_one(session_data)

    new_session = await db["chatsessions"].find_one({"_id": result.inserted_id})

    if new_session:
        new_session["id"] = str(new_session["_id"])
        new_session.pop("_id", None)

    return new_session


async def get_session_by_id(db, id: str):

    sessionId_obj = ObjectId(id)

    session = await db["chatsessions"].find_one({"_id": sessionId_obj})

    if session:
        session["id"] = str(session["_id"])
        session.pop("_id", None)

    return session


async def save_session(db, session: Dict):
    result = await db["chatsessions"].update_one(
        {"_id": ObjectId(session["id"])}, {"$set": session}, upsert=True
    )

    return result


async def update_title(db, session: Dict, title: str):
    print("session: ", session)
    print("title: ", title)
    result = await db["chatsessions"].update_one(
        {"_id": ObjectId(session["id"])}, {"$set": {"title": title}}, upsert=True
    )

    return result


async def delete_session(db, session: Dict):
    result = await db["chatsessions"].delete_one({"_id": ObjectId(session["id"])})

    return result
