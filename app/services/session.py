from fastapi import HTTPException, status, Response, Cookie, Depends, Request
from passlib.context import CryptContext
from .auth import verify_token
from app.core.database import get_db
from typing import List
from ..schemas.session import ShowSession, CreateSession, Session, UpdateTitle
from ..schemas.chat import ShowChat, ListChat
from ..crud.session import (
    list_sessions_by_user,
    create_session_by_user,
    get_session_by_id,
    save_session,
    update_title,
    delete_session,
)
from ..schemas.chat import ChatRequest, CreateChat
from datetime import datetime, timezone
from app.core.openai import configure_gemini
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from ..utils.index import convert_objectid_to_str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def list_sessions_logic(
    db=Depends(get_db), existing_user: dict = Depends(verify_token)
):
    # 1. Tìm list session by userId
    userId = existing_user["id"]
    sessions = await list_sessions_by_user(db, userId)

    # 2. Return response
    return [ShowSession(**session) for session in sessions]


async def create_session_logic(
    db=Depends(get_db),
    existing_user: dict = Depends(verify_token),
):
    # 1. Tạo session trong db
    userId = existing_user["id"]

    session = await create_session_by_user(db, userId)
    # 2. Return response
    return ShowSession(message="Ok", id=session["id"], title=session["title"])


async def create_message_logic(
    chat_request: ChatRequest,
    sessionId: str,
    db=Depends(get_db),
    existing_user: dict = Depends(verify_token),
):
    # 1. Kiểm tra sessionId có tồn tại không?
    session = await get_session_by_id(db, sessionId)
    if not session:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Session not exists")

    # 2. Lưu thêm message vào session
    new_chat = CreateChat(
        role="user", content=chat_request.message, createdAt=datetime.now(timezone.utc)
    )

    try:
        session["chats"].append(new_chat.dict())
        await save_session(db, session)
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Fails append new chat")

    # 3. Generate câu trả lời từ AI
    chats_for_gemini = [
        {"role": chat["role"], "parts": [{"text": chat["content"]}]}
        for chat in session["chats"]
    ]

    genai = configure_gemini()
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    result = model.generate_content(contents=chats_for_gemini)
    text = result.text

    assistant_chat = CreateChat(
        role="assistant", content=text, createdAt=datetime.now(timezone.utc)
    )

    try:
        session["chats"].append(assistant_chat.dict())
        await save_session(db, session)
    except:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Fails append assistant chat"
        )

    # Chuyển đổi ObjectId thành chuỗi trước khi trả về
    session_chats = convert_objectid_to_str(session["chats"])

    show_chats = [
        ShowChat(
            role=chat["role"],
            content=chat["content"],
            createdAt=chat["createdAt"],
        )
        for chat in session_chats
    ]

    # Trả về session đã được mã hóa
    return show_chats


async def list_chat_session_logic(
    sessionId: str, db=Depends(get_db), existing_user: dict = Depends(verify_token)
):
    # 1. Kiểm tra sesion có trong db không
    session = await get_session_by_id(db, sessionId)
    if not session:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Session not exists")

    # 2. Kiểm tra existing_user có đúng với author của session không
    if str(session["userId"]) != str(existing_user["id"]):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Permissions diddn't match"
        )

    # 3. Lấy chat từ session
    session_chats = convert_objectid_to_str(session["chats"])

    show_chats = [
        ShowChat(
            role=chat["role"],
            content=chat["content"],
            createdAt=chat["createdAt"],
        )
        for chat in session_chats
    ]

    # 4. return response

    return ListChat(message="Ok", chats=session_chats)


async def update_title_session_logic(
    sessionId: str,
    message: UpdateTitle,
    db=Depends(get_db),
    existing_user: dict = Depends(verify_token),
):
    # 1. Kiểm tra session có tồn tại trong db không?
    session = await get_session_by_id(db, sessionId)
    if not session:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Session not exists")

    # 2. Kiêm tra xem có permissions không?
    if str(session["userId"]) != str(existing_user["id"]):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Permissions diddn't match"
        )
    # 3. Update title session vào db
    result = await update_title(db, session, message.title)
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Session not found or title unchanged"
        )
    # 4. Return response

    return {"message": "Ok"}


async def delete_session_logic(
    sessionId: str, db=Depends(get_db), existing_user: dict = Depends(verify_token)
):

    # 1. Kiểm tra permissions user
    session = await get_session_by_id(db, sessionId)
    if str(session["userId"]) != str(existing_user["id"]):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Permissions diddn't match"
        )

    # 2. Thực hiện xóa trong db
    result = await delete_session(db, session)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")

    # 3. Return response
    return {"message": "Session deleted successfully"}
