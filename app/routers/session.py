from fastapi import APIRouter, Depends, Request
from ..schemas.session import ShowSession, UpdateTitle
from ..schemas.chat import ShowChat, ChatRequest, ListChat
from app.core.database import get_db
from typing import List, Dict
from ..services.session import (
    list_sessions_logic,
    create_session_logic,
    create_message_logic,
    list_chat_session_logic,
    update_title_session_logic,
    delete_session_logic,
)

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get(
    "/user",
    response_model=List[ShowSession]
)
async def list_sessions(list_sessions_response: List = Depends(list_sessions_logic)):
    return list_sessions_response


@router.post("/", response_model=ShowSession)
async def create_session(create_session_response: dict = Depends(create_session_logic)):
    return create_session_response


@router.post("/{sessionId}/messages", response_model=List[ShowChat])
async def create_message(
    create_message_response: dict = Depends(create_message_logic),
):
    return create_message_response


@router.get("/{sessionId}", response_model=ListChat)
async def list_chat_session(
    list_chat_session_response: List = Depends(list_chat_session_logic),
):
    return list_chat_session_response


@router.patch("/{sessionId}", response_model=Dict)
async def update_title_session(
    response_update: dict = Depends(update_title_session_logic),
):
    return response_update


@router.delete("/{sessionId}", response_model=Dict)
async def delete_session(response_delete: dict = Depends(delete_session_logic)):
    return response_delete
